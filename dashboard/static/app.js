const paths = ["/health", "/version", "/environment"];

function fmt(ms) {
  return ms.toFixed(0) + " ms";
}

async function ping(path) {
  const t0 = performance.now();
  try {
    const res = await fetch(path, { cache: "no-store" });
    const body = await res.json();
    return {
      path,
      status: res.status,
      ms: performance.now() - t0,
      body: JSON.stringify(body),
      json: body,
      ok: res.ok,
    };
  } catch (err) {
    return {
      path,
      status: 0,
      ms: performance.now() - t0,
      body: String(err),
      json: {},
      ok: false,
    };
  }
}

function setText(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
}

async function refresh() {
  const results = await Promise.all(paths.map(ping));
  const rows = results
    .map((r) => {
      const cls = r.ok ? "code-ok" : "code-bad";
      return `<tr>
        <td>${r.path}</td>
        <td class="${cls}">${r.status || "err"}</td>
        <td>${fmt(r.ms)}</td>
        <td>${r.body}</td>
      </tr>`;
    })
    .join("");
  document.getElementById("rows").innerHTML = rows;

  const health = results[0];
  const version = results[1];
  const env = results[2];
  const up = health.ok && health.json.status === "UP";

  const hero = document.getElementById("hero-status");
  hero.textContent = up ? "UP" : "DOWN";
  hero.className = "hero-status " + (up ? "up" : "down");
  setText("hero-meta", up ? "all required endpoints returned 200" : "one or more checks failed");
  setText("health-value", health.json.status || "DOWN");
  setText("health-hint", up ? "GET /health · ok" : "GET /health · failed");
  if (version.json.version) setText("version-value", version.json.version);
  if (env.json.environment) {
    setText("env-value", env.json.environment);
    setText("env-pill", env.json.environment);
  }
  setText("clock", new Date().toLocaleTimeString());
}

refresh();
setInterval(refresh, 5000);

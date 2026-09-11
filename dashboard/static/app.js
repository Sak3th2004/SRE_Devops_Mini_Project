const paths = ["/health", "/version", "/environment", "/ready"];

function fmt(ms) {
  return Math.round(ms) + " ms";
}

function setText(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
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
      json: body,
      ok: res.ok,
    };
  } catch (err) {
    return { path, status: 0, ms: performance.now() - t0, json: {}, ok: false };
  }
}

function uptimeText(sec) {
  const h = Math.floor(sec / 3600);
  const m = Math.floor((sec % 3600) / 60);
  const s = sec % 60;
  if (h) return h + "h " + m + "m";
  if (m) return m + "m " + s + "s";
  return s + "s";
}

async function refresh() {
  const results = await Promise.all(paths.map(ping));
  const extra = await Promise.all(["/slo", "/info", "/deps", "/events"].map(ping));
  const slo = extra[0].json || {};
  const info = extra[1].json || {};
  const deps = extra[2].json || {};
  const events = extra[3].json || {};

  document.getElementById("rows").innerHTML = results
    .map((r) => {
      const cls = r.ok ? "code-ok" : "code-bad";
      const body = r.json && Object.keys(r.json).length
        ? JSON.stringify(r.json)
        : "—";
      return `<tr>
        <td>${r.path}</td>
        <td class="${cls}">${r.status || "err"}</td>
        <td>${fmt(r.ms)}</td>
        <td class="json">${body}</td>
      </tr>`;
    })
    .join("");

  const health = results[0];
  const version = results[1];
  const env = results[2];
  const up = health.ok && health.json.status === "UP";

  const hero = document.getElementById("hero-status");
  hero.textContent = up ? "UP" : "DOWN";
  hero.className = "hero-status " + (up ? "up" : "down");
  setText("hero-meta", up ? "required checks returned 200" : "a required check failed");
  setText("health-value", health.json.status || "DOWN");
  if (version.json.version) setText("version-value", version.json.version);
  if (env.json.environment) {
    setText("env-value", env.json.environment);
    setText("env-pill", env.json.environment);
  }

  const dot = document.getElementById("live-dot");
  dot.className = "dot " + (up ? "on" : "off");
  setText("live-label", up ? "live" : "down");
  if (info.uptime_seconds != null) setText("uptime", uptimeText(info.uptime_seconds));
  if (info.hostname) setText("host", info.hostname);
  if (info.environment || info.hostname) {
    setText("runtime", "instance " + (info.hostname || "unknown"));
  }

  if (slo.availability_pct != null) {
    setText("slo-value", slo.availability_pct + "%");
    const counts = (slo.good != null)
      ? slo.good + " good / " + slo.bad + " bad · target " + slo.target + "%"
      : "target " + slo.target + "%";
    setText("slo-hint", counts);
    const left = slo.budget_remaining_pct;
    setText("budget-label", left + "% remaining");
    const bar = document.getElementById("budget-bar");
    bar.style.width = Math.min(100, left) + "%";
    bar.className = "bar" + (left < 20 ? " bad" : left < 50 ? " warn" : "");
  }

  const names = { prometheus: "Prometheus", jenkins: "Jenkins", api: "API" };
  document.getElementById("deps").innerHTML = Object.keys(names)
    .map((key) => {
      const item = deps[key] || {};
      const ok = !!item.ok;
      return `<li><span>${names[key]}</span><span class="${ok ? "code-ok" : "code-bad"}">${ok ? "up" : "down"}</span></li>`;
    })
    .join("");

  const items = Array.isArray(events.items) ? events.items.slice(0, 12) : [];
  document.getElementById("events").innerHTML = items.length
    ? items.map((item) => {
        const cls = item.ok ? "code-ok" : "code-bad";
        return `<tr>
          <td>${item.ts || "—"}</td>
          <td>${item.path || "—"}</td>
          <td class="${cls}">${item.status || "err"}</td>
          <td>${item.ms != null ? item.ms + " ms" : "—"}</td>
        </tr>`;
      }).join("")
    : `<tr><td colspan="4">no requests recorded yet</td></tr>`;

  setText("clock", new Date().toLocaleTimeString());
}

refresh();
setInterval(refresh, 5000);

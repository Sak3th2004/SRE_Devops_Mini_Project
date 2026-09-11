# System Health Dashboard
C456 SRE mini project

Ops API plus the delivery path: Git, tests, Docker, Jenkins, Kubernetes, Prometheus, Grafana.

PDF endpoints stay as specified. Extra routes cover SLO, dependencies and process info.

## Endpoints

| Path | Notes |
|---|---|
| `GET /` | dashboard |
| `GET /health` | `{"status": "UP"}` |
| `GET /version` | app version |
| `GET /environment` | `APP_ENV` |
| `GET /ready` | process check |
| `GET /metrics` | Prometheus |
| `GET /info` | uptime, host, version |
| `GET /slo` | availability and error budget |
| `GET /deps` | Prometheus + Jenkins probes |
| `GET /events` | recent request samples |

`APP_ENV` is not hard-coded.

## Layout

```
app.py
dashboard/
  config.py
  health.py      /health /version /environment /ready /metrics
  ops.py         /info /slo /deps /events
  ui.py
  store.py
  metrics.py
tests/
Dockerfile
Jenkinsfile
docker-compose.yml     api + prometheus + grafana
k8s/                   student-11
monitoring/
docs/
```

## Local (Docker Desktop)

```
docker compose up --build
```

- App: http://127.0.0.1:5000
- Grafana: http://127.0.0.1:3000  (admin / admin)
- Local Prometheus: http://127.0.0.1:9091
- Trainer Prometheus: http://43.205.104.60:9090

Grafana has two datasources: local scrape of this API, and the class Prometheus for node/k8s.

Without compose:

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
set APP_ENV=development
python app.py
```

```
pytest -q
```

## Jenkins

http://3.6.114.43:8080/

`Jenkinsfile` stages: Checkout → Install → Test → Build → Tag → Health check (also hits `/ready` `/slo` `/info`).

Point a Pipeline job at this repo. Screenshot one failed run (break a test) and one green run.

## Kubernetes

Namespace `student-11`. Do not delete `devbox`.

```
kubectl apply -n student-11 -f k8s/
```

App image is `system-health-dashboard:1.0.0` (`IfNotPresent`). Grafana YAML is there if you want it in-cluster as well; Docker Desktop Grafana is enough for the demo.

```
kubectl -n student-11 port-forward svc/health-dashboard 5000:5000
```

## Git / PR

`main`, `develop`, `feature/*`. Conflict notes: `docs/merge-conflict.md`.

Open a PR develop → main and review it from a second GitHub account: `docs/pr-review.md`.

## Other notes

- SLO: `docs/slo.md`
- Demo order: `docs/demo.md`
- Sandbox URLs: `docs/sandbox.md`

No kubeconfig, tokens or `.env` files in git.

# System Health Dashboard

C456 SRE mini project: health APIs plus Git, tests, Docker, Jenkins, Kubernetes, Prometheus and Grafana.

`APP_ENV` is not hard-coded. Extra routes cover SLO, dependencies and process info.

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

## Layout

```
app.py
dashboard/             APIs, UI, metrics
tests/test_app.py
scripts/traffic.py     load against a running app
Dockerfile
docker-compose.yml     api + prometheus + grafana
Jenkinsfile
k8s/                   student-11 (configmap, deployment, service)
monitoring/            local Prometheus + Grafana
docs/                  merge-conflict, PR review, SLO, reflection
```

## Local

```
docker compose up --build
```

- App: http://127.0.0.1:5000  (`APP_ENV=development`)
- Grafana: http://127.0.0.1:3000  (admin / admin)
- Local Prometheus: http://127.0.0.1:9091

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
python3 scripts/traffic.py --url http://127.0.0.1:5000 --seconds 60
```

The image is built on this machine. It is not pushed to a registry.

## Jenkins

http://3.6.114.43:8080/ job `system-health-platform-saketh`

Stages: Checkout → Install → Test → Build → Tag → Health check.

This agent has no Docker daemon, so Build/Tag fall back to a source archive. The pipeline does not push an image and does not deploy to Kubernetes.

## Kubernetes

Namespace `student-11`. One replica. ConfigMap sets `APP_ENV=production`.

```
kubectl apply -f k8s/configmap.yaml -f k8s/deployment.yaml -f k8s/service.yaml
kubectl -n student-11 port-forward svc/health-dashboard 5001:5000
```

The pod uses `python:3.12-slim`, clones GitHub `main`, then runs gunicorn. Do not apply `k8s/grafana.yaml` on the cluster.

## Git

`main`, `develop`, `feature/*`. Conflict notes: `docs/merge-conflict.md`. PR review: `docs/pr-review.md`. SLO: `docs/slo.md`.

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
| `GET /ready` | process plus Prometheus/Jenkins probes |
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

Stages: Checkout → Install → Test → Build → Tag → Publish → Health check.

This agent has no Docker daemon, so Build/Tag/Publish fall back and stay green. The pipeline does not push to a registry and does not deploy to Kubernetes. The cluster image is built on this laptop and loaded with `kind load`.

## Kubernetes

Namespace `student-11`. One replica. ConfigMap sets `APP_ENV=production`.

The pod runs image `system-health-dashboard:1.0.0` (no git clone). Load it into kind, then apply:

```
bash scripts/release-k8s.sh
kubectl --kubeconfig /tmp/sre-prep.kubeconfig -n student-11 port-forward svc/health-dashboard 5001:5000
```

Use the `kind-sre-prep` kubeconfig. Do not switch to context `default`. Do not apply `k8s/grafana.yaml`.

Local Prometheus scrapes the Docker app and the kind NodePort (`sre-prep-control-plane:30080`).

## Git

`main`, `develop`, `feature/*`. Conflict notes: `docs/merge-conflict.md`. PR review: `docs/pr-review.md`. SLO: `docs/slo.md`.

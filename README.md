# System Health Dashboard
C456 SRE mini project — Git to deployment

Small API for the ops team. It answers three questions: is the service up, which version is running, and which environment is this. Git, tests, Docker and Jenkins are the marked work. Kubernetes and Grafana sit on the trainer sandbox.

## What it does

| Endpoint | Response |
|---|---|
| `GET /` | dashboard page |
| `GET /health` | `{"status": "UP"}` |
| `GET /version` | app version |
| `GET /environment` | value of `APP_ENV` |
| `GET /metrics` | Prometheus metrics |

Environment is read from `APP_ENV`. It is not hard-coded.

## Layout

```
app.py                 entrypoint
dashboard/             app package
  config.py
  routes.py
  metrics.py
  templates/
  static/
tests/test_app.py
Dockerfile
Jenkinsfile
k8s/                   student-11 manifests
monitoring/            grafana dashboard + scrape snippet
docs/
```

## Run locally

Python 3.12+

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
set APP_ENV=development
set APP_VERSION=1.0.0
python app.py
```

On WSL / Linux:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
APP_ENV=development APP_VERSION=1.0.0 python app.py
```

Open http://127.0.0.1:5000

```
curl http://127.0.0.1:5000/health
curl http://127.0.0.1:5000/version
curl http://127.0.0.1:5000/environment
```

## Tests

```
pytest -q
```

That is the one command for the full suite.

## Docker

```
docker build -t system-health-dashboard:1.0.0 .
docker run --rm -p 5000:5000 -e APP_ENV=production -e APP_VERSION=1.0.0 system-health-dashboard:1.0.0
```

Or `docker compose up --build`

## Jenkins

Pipeline lives in `Jenkinsfile`. Use the class Jenkins:

http://3.6.114.43:8080/

Stages: Checkout → Install → Test → Build → Tag → Health check

Create a Pipeline job, point it at this repo, script path `Jenkinsfile`. Screenshot a green build. To show failure handling, break one assert in `tests/test_app.py`, run once, then put it back.

Image tag includes the Jenkins build number (`1.0.$BUILD_NUMBER`).

## Kubernetes

Namespace: `student-11` (already created). Do not delete the `devbox` pod.

```
kubectl apply -n student-11 -f k8s/configmap.yaml
kubectl apply -n student-11 -f k8s/deployment.yaml
kubectl apply -n student-11 -f k8s/service.yaml
```

The deployment expects image `system-health-dashboard:1.0.0` on the node (`IfNotPresent`). Build it, then load it into k3s if the node does not have it:

```
docker save system-health-dashboard:1.0.0 -o health.tar
# copy onto the k3s node, then:
sudo k3s ctr images import health.tar
```

If NodePort is open: `http://<node-ip>:30080`

Otherwise:

```
kubectl -n student-11 port-forward svc/health-dashboard 5000:5000
```

## Grafana

Trainer Grafana was down. This repo deploys Grafana in `student-11` and points it at the existing Prometheus.

```
kubectl apply -n student-11 -f k8s/grafana.yaml
kubectl apply -n student-11 -f k8s/grafana-dashboard.yaml
kubectl -n student-11 rollout restart deploy/grafana
```

Login: `admin` / `admin`

```
kubectl -n student-11 port-forward svc/grafana 3000:3000
```

http://127.0.0.1:3000 — dashboard **C456 System Health**.

Prometheus (already running): http://43.205.104.60:9090/

Optional scrape of the API: `monitoring/prometheus-scrape.yml`. Only add it if you can edit prometheus.yml on the trainer host.

## Git

- `main` — release
- `develop` — integration
- `feature/*` — work branches

See `docs/merge-conflict.md` for the conflict we resolved. Open a PR from `develop` into `main` and get a review before merge.

## Reflection

`docs/reflection.md`

## Sandbox

| Thing | Where |
|---|---|
| Jenkins | http://3.6.114.43:8080/ |
| Prometheus | http://43.205.104.60:9090/ |
| k8s namespace | student-11 |
| Grafana | pod in student-11 |

No kubeconfig files, tokens or `.env` files are committed.

Tools used: editor, Docker docs, Jenkins pipeline docs, Grafana provisioning docs.

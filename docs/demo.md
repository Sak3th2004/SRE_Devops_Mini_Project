# Live demo (about 6 minutes)

Start the stack **before** he sits down. Then only click and talk. Do not install anything during the demo.

## Before he arrives (2 minutes)

Open **three** terminals. Stay on the cluster that already worked (`sre-prep`), not context `default`.

Terminal A — app + Grafana on your laptop:

```
cd /mnt/c/Users/saketh/Mini_Project
docker compose up -d
```

Terminal B — Kubernetes:

```
cd /mnt/c/Users/saketh/Mini_Project
kubectl get pods -n student-11
kubectl -n student-11 port-forward svc/health-dashboard 5001:5000
```

Leave B running.

Terminal C — keep free for `pytest` and `kubectl`.

Quick check (browser):

- http://127.0.0.1:5000  (Docker)
- http://127.0.0.1:5001  (Kubernetes)
- http://127.0.0.1:3000  (Grafana, admin / admin)
- http://3.6.114.43:8080/job/system-health-platform-saketh/
- http://43.205.104.60:9090/

If 5001 fails, use 5000 only and say the pod is still in `kubectl get pods`.

## Minute 1 — what it is

Open the GitHub repo on branch `main`.

Say:

This is a System Health Dashboard for the ops team. Three required APIs: health, version, environment. Environment comes from APP_ENV, not from code. Rest of the work is Git, tests, Docker, Jenkins, then Kubernetes and Grafana.

Show `app.py` and `dashboard/` folders.

## Minute 2 — Git

Open:

- branches (`main`, `develop`, `feature/...`)
- PR https://github.com/Sak3th2004/SRE_Devops_Mini_Project/pull/1
- `docs/merge-conflict.md`

Say:

I used feature branches into develop, then a PR into main. Two branches both changed the version default. I resolved it to 1.0.0. sakethram00 reviewed the PR before merge.

## Minute 3 — tests and a failed pipeline

Terminal C:

```
cd /mnt/c/Users/saketh/Mini_Project
pytest -q
```

Expect 8 passed.

Then Jenkins: job `system-health-platform-saketh`.

Show build **#1 or #2** (red) and build **#3** (green).

Say:

Checkout worked first. Install failed because this Jenkins has no python and no docker — it runs inside a container. I changed the Jenkinsfile so Install, Test and Health run without a docker daemon. After that, build 3 is green. Failed stages stop the rest of the pipeline.

## Minute 4 — Docker and the API

Browser: http://127.0.0.1:5000

```
curl http://127.0.0.1:5000/health
curl http://127.0.0.1:5000/version
curl http://127.0.0.1:5000/environment
```

Say:

Same image via Docker Compose. APP_ENV is development here. On Kubernetes I set production through a ConfigMap.

Open http://127.0.0.1:5001 and point at production and the pod hostname.

## Minute 5 — Jenkins green + Grafana + k8s

Jenkins: green build #3, stages Checkout, Install, Test, Build, Tag, Health check.

Grafana: http://127.0.0.1:3000 dashboard C456 System Health.

Say:

Grafana is on my machine because the class Grafana was removed. Datasource is the class Prometheus at 43.205.104.60:9090. You can see node exporter and request rate.

Terminal C:

```
kubectl get pods -n student-11
```

Say:

Namespace student-11, one replica, probes on /health.

## Last 20 seconds — one improvement

Say:

If I put this in production I would mount Docker on the Jenkins agent so the same pipeline builds and tags the image there, then the cluster pulls that tag. Image load is still the manual step.

Stop. Do not open more tabs.

## If something is down

| Thing | Fallback |
|---|---|
| Port 5001 | Use 5000 only |
| Grafana | Show Prometheus http://43.205.104.60:9090/targets |
| Jenkins | Screenshot of #3 |
| kubectl | Screenshot of 1/1 Running |

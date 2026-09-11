# Demo (5 min)

1. Repo: branches, one merge conflict (`docs/merge-conflict.md`), PR.
2. `pytest -q` and the Jenkins red/green screenshots.
3. Docker: `docker compose up --build` then http://127.0.0.1:5000 (`/health` `/version` `/environment` plus `/slo` `/deps`).
4. Grafana: http://127.0.0.1:3000 (admin/admin) — C456 System Health. Trainer Prometheus at http://43.205.104.60:9090 is the second datasource.
5. `kubectl get pods -n student-11` — leave `devbox`, show our deploy if applied.

One improvement: push the Jenkins image to a registry so k8s pulls the same tag.

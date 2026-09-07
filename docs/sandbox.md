# Sandbox

Do not recreate Jenkins or Prometheus. Use the class ones.

Jenkins: http://3.6.114.43:8080/
Prometheus: http://43.205.104.60:9090/

Prometheus is already scraping:

- node-exporter on 10.0.1.220:32189
- kube-state-metrics / k3s on 10.0.1.220:32517
- prometheus itself

Grafana on :3000 was not running. We deploy Grafana into namespace student-11.

k8s: k3s, namespace student-11, existing pod `devbox-...` — leave it.

Postgres is up on the trainer side. This API does not need it for the marked endpoints.

# Reflection

Which Git practice most improved the way you organised your work?

Feature branches. API work stayed off Docker/Jenkins until the endpoints were actually returning 200. Easier to review that way.

Where did automation detect or prevent an error?

The Test stage. I broke one assert on purpose; Jenkins stopped before Build/Tag. That is the point of putting tests before the image.

What would you change before using this workflow in production?

Push the image Jenkins builds to a registry and have the k8s deployment pull that tag. Right now the cluster image is loaded by hand (`IfNotPresent`), which will drift.

Which step still depends on manual action, and how could it be automated?

Grafana datasource is provisioned, but adding the API scrape job on the trainer Prometheus host is still manual. A ServiceMonitor (or a second scrape file the host already watches) would close that gap. Image load onto k3s is also still manual.

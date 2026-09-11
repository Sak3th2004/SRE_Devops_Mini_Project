# SLO

SLI: share of HTTP responses with status < 400.

SLO: 99.5% availability over the process lifetime (good enough for the lab).

Error budget: 0.5%. `/slo` returns current availability and how much budget is left.

If budget remaining drops under 20% the dashboard bar turns red. Alerts live in `monitoring/alerts.yml` (AppDown, HighErrorRate).

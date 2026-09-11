import time

from flask import request, Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

from dashboard import store

REQUESTS = Counter(
    "http_requests_total",
    "HTTP requests",
    ["method", "path", "status"],
)
LATENCY = Histogram(
    "http_request_duration_seconds",
    "Request duration in seconds",
    ["path"],
)
APP_UP = Gauge("app_up", "Process is up")
APP_INFO = Gauge(
    "app_info",
    "App metadata",
    ["version", "environment"],
)

SKIP_STORE = {"/metrics", "/static"}


def setup_metrics(app):
    APP_UP.set(1)
    APP_INFO.labels(
        version=app.config["APP_VERSION"],
        environment=app.config["APP_ENV"],
    ).set(1)

    @app.before_request
    def _mark_start():
        request._started = time.time()

    @app.after_request
    def _record(resp):
        path = request.path
        started = getattr(request, "_started", None)
        ms = (time.time() - started) * 1000 if started is not None else 0
        if not path.startswith("/static") and path != "/metrics":
            REQUESTS.labels(request.method, path, str(resp.status_code)).inc()
            if started is not None:
                LATENCY.labels(path).observe(ms / 1000.0)
            store.record(path, 200 <= resp.status_code < 400, resp.status_code, ms)
        return resp


def metrics_response():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

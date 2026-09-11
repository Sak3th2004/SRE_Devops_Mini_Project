from flask import Blueprint, current_app, jsonify

from dashboard.metrics import metrics_response
from dashboard.probes import dependency_checks

bp = Blueprint("health", __name__)


@bp.get("/health")
def health():
    return jsonify(status="UP")


@bp.get("/version")
def version():
    return jsonify(version=current_app.config["APP_VERSION"])


@bp.get("/environment")
def environment():
    return jsonify(environment=current_app.config["APP_ENV"])


@bp.get("/ready")
def ready():
    checks = dependency_checks(current_app)
    process_ok = bool(checks.get("process", {}).get("ok"))
    all_ok = all(bool(item.get("ok")) for item in checks.values())
    payload = {
        "status": "UP" if all_ok else "DEGRADED",
        "ready": process_ok,
        "checks": checks,
    }
    # Process up => HTTP 200 so Jenkins and kube probes do not fail when Jenkins/Prometheus lag.
    return jsonify(payload), 200 if process_ok else 503


@bp.get("/metrics")
def metrics():
    return metrics_response()

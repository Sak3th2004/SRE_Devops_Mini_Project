import platform
import socket

from flask import Blueprint, current_app, jsonify

from dashboard import store
from dashboard.probes import dependency_checks

bp = Blueprint("ops", __name__)


@bp.get("/info")
def info():
    return jsonify(
        service="system-health-dashboard",
        version=current_app.config["APP_VERSION"],
        environment=current_app.config["APP_ENV"],
        uptime_seconds=store.uptime_seconds(),
        hostname=socket.gethostname(),
        python=platform.python_version(),
        namespace=current_app.config["K8S_NAMESPACE"],
    )


@bp.get("/slo")
def slo():
    data = store.slo_snapshot(current_app.config["SLO_TARGET"])
    data["window"] = "process lifetime"
    data["sli"] = "successful HTTP responses / total HTTP responses"
    return jsonify(data)


@bp.get("/deps")
def deps():
    checks = dependency_checks(current_app)
    return jsonify(
        prometheus=checks["prometheus"],
        jenkins=checks["jenkins"],
        api=checks["api"],
    )


@bp.get("/events")
def events():
    return jsonify(items=store.recent_events())

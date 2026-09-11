import platform
import socket
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from flask import Blueprint, current_app, jsonify

from dashboard import store

bp = Blueprint("ops", __name__)


def _probe(url, timeout=2):
    try:
        with urlopen(url, timeout=timeout) as resp:
            code = getattr(resp, "status", 200)
            return {"ok": True, "status": code}
    except HTTPError as err:
        return {"ok": err.code < 500, "status": err.code}
    except URLError as err:
        return {"ok": False, "error": str(err.reason) if getattr(err, "reason", None) else str(err)}
    except Exception as err:
        return {"ok": False, "error": str(err)}


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
    prom = current_app.config["PROMETHEUS_URL"].rstrip("/")
    jenkins = current_app.config["JENKINS_URL"].rstrip("/")
    return jsonify(
        prometheus=_probe(prom + "/-/ready"),
        jenkins=_probe(jenkins + "/login"),
        api={"ok": True, "status": 200},
    )


@bp.get("/events")
def events():
    return jsonify(items=store.recent_events())

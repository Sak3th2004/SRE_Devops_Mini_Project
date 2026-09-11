from flask import Blueprint, current_app, jsonify

from dashboard.metrics import metrics_response

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
    return jsonify(status="UP", checks={"process": "ok"})


@bp.get("/metrics")
def metrics():
    return metrics_response()

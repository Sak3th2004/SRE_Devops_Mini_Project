from flask import Blueprint, current_app, jsonify, render_template

from dashboard.metrics import metrics_response

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    return render_template(
        "index.html",
        environment=current_app.config["APP_ENV"],
        version=current_app.config["APP_VERSION"],
    )


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

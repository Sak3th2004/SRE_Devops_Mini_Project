from flask import Blueprint, current_app, render_template

bp = Blueprint("ui", __name__)


@bp.get("/")
def index():
    return render_template(
        "index.html",
        environment=current_app.config["APP_ENV"],
        version=current_app.config["APP_VERSION"],
        slo_target=current_app.config["SLO_TARGET"],
        namespace=current_app.config["K8S_NAMESPACE"],
    )

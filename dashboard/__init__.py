import logging
import os

from flask import Flask

from dashboard.config import Config
from dashboard.health import bp as health_bp
from dashboard.metrics import setup_metrics
from dashboard.ops import bp as ops_bp
from dashboard.ui import bp as ui_bp


def create_app():
    here = os.path.dirname(__file__)
    app = Flask(
        __name__,
        template_folder=os.path.join(here, "templates"),
        static_folder=os.path.join(here, "static"),
    )
    app.config.from_object(Config)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    setup_metrics(app)
    app.register_blueprint(ui_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(ops_bp)
    return app

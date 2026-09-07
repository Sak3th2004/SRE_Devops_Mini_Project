import os

from flask import Flask

from dashboard.config import Config
from dashboard.metrics import setup_metrics
from dashboard.routes import bp


def create_app():
    here = os.path.dirname(__file__)
    app = Flask(
        __name__,
        template_folder=os.path.join(here, "templates"),
        static_folder=os.path.join(here, "static"),
    )
    app.config.from_object(Config)
    setup_metrics(app)
    app.register_blueprint(bp)
    return app

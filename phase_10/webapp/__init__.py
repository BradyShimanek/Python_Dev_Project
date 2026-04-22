from flask import Flask

from .database import init_database
from .routes import web


def create_app() -> Flask:
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config["SECRET_KEY"] = "dev"
    init_database()
    app.register_blueprint(web)
    return app

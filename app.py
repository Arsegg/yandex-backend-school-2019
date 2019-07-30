from flask import Flask

from ext import db
from imports import imports


def create_app():
    app = Flask(__name__)
    app.config["MONGODB_SETTINGS"] = {
        "host": "mongodb://db/imports",
        "connect": False,
    }
    db.init_app(app)

    app.register_blueprint(imports, url_prefix="/imports")

    return app

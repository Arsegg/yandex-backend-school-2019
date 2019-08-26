from flask import Flask

from ext import (db,
                 ma, )
from imports import imports


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@db/postgres"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.app_context().push()

    db.init_app(app)
    db.drop_all()
    db.create_all()
    db.session.commit()

    ma.init_app(app)

    app.register_blueprint(imports)

    return app

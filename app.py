from flask import Flask

from imports import imports


def create_app():
    app_ = Flask(__name__)
    app_.register_blueprint(imports, url_prefix="/imports")
    return app_


if __name__ == "__main__":
    app = create_app()
    app.run()

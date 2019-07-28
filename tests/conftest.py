from pytest import fixture


@fixture
def app():
    from app import app
    return app

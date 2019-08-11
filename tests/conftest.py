from flask import url_for
from pytest import fixture

from app import create_app


@fixture
def app():
    return create_app()


@fixture
def unwrap():
    return lambda response: response.get_json()["data"]


@fixture
def post(client):
    return lambda json: client.post(url_for("imports.post"), json=json)


@fixture
def patch_citizens(client):
    return lambda import_id, citizen_id, json: client.patch(
        url_for("imports.patch_citizens", import_id=import_id, citizen_id=citizen_id), json=json)


@fixture
def get_citizens(client):
    return lambda import_id: client.get(url_for("imports.get_citizens", import_id=0))


@fixture
def get_citizens_birthdays(client):
    return lambda import_id: client.get(url_for("imports.get_citizens_birthdays", import_id=0))


@fixture
def get_towns_stat_percentile_age(client):
    return lambda import_id: client.get(url_for("imports.get_towns_stat_percentile_age", import_id=0))

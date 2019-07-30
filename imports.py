from bson.errors import InvalidId
from bson.objectid import ObjectId
from flask import Blueprint
from flask import abort
from flask import request
from json.decoder import JSONDecodeError

from models import Import

imports = Blueprint("imports", __name__)


def to_int(object_id):
    """TODO: refactor as ImportIdField.to_python"""
    return int(str(object_id), 16)


def to_object_id(import_id):
    """TODO: refactor as ImportIdField.to_mongo"""
    return ObjectId(f"{import_id:x}")


@imports.route("", methods=("POST",))
def post():
    try:
        data = request.get_data()
        citizens = Import.from_json(data)
        import_id = citizens.save().id
    except JSONDecodeError:
        abort(400)
    return dict(data=dict(import_id=to_int(import_id))), 201


@imports.route("/<int:import_id>/citizens/<int:citizen_id>", methods=("PATCH",))
def patch_citizens(import_id, citizen_id):
    """TODO"""
    citizen = {}
    return dict(data=citizen), 200


@imports.route("/<int:import_id>/citizens", methods=("GET",))
def get_citizens(import_id):
    try:
        citizens = Import.objects(id=to_object_id(import_id)).first().citizens
        return dict(data=citizens), 200
    except InvalidId:
        abort(400)


@imports.route("/<int:import_id>/citizens/birthdays", methods=("GET",))
def get_citizens_birthdays(import_id):
    """"TODO"""
    birthdays = {}
    return dict(data=birthdays), 200


@imports.route("/<int:import_id>/towns/stat/percentile/age", methods=("GET",))
def get_towns_stat_percentile_age(import_id):
    """"TODO"""
    stats = []
    return dict(data=stats), 200

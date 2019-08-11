from flask import Blueprint

imports = Blueprint("imports", __name__)


@imports.route("", methods=("POST",))
def post():
    """TODO"""
    import_id = 0
    return dict(data=dict(import_id=import_id)), 201


@imports.route("/<int:import_id>/citizens/<int:citizen_id>", methods=("PATCH",))
def patch_citizens(import_id, citizen_id):
    """TODO"""
    citizen = {}
    return dict(data=citizen), 200


@imports.route("/<int:import_id>/citizens", methods=("GET",))
def get_citizens(import_id):
    """TODO"""
    citizens = []
    return dict(data=citizens), 200


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

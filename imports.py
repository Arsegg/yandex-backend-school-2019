from flask import (Blueprint,
                   request, )

from ext import (db,
                 )
from models import (Citizen,
                    Import,
                    citizen_schema,
                    citizens_schema,
                    import_schema, )

imports = Blueprint("imports", __name__, url_prefix="/imports")


@imports.route("", methods=("POST",))
def post():
    """TODO: add verifiers"""
    import_ = import_schema.load(request.get_json())
    db.session.add(import_)
    db.session.commit()

    import_id = import_.import_id

    return dict(data=dict(import_id=import_id)), 201


@imports.route("/<int:import_id>/citizens/<int:citizen_id>", methods=("PATCH",))
def patch_citizens(import_id, citizen_id):
    """TODO: ensure relationship"""
    instance = Citizen.query.filter_by(import_id=import_id, citizen_id=citizen_id).one()
    citizen = citizen_schema.load(request.get_json(),
                                  instance=instance,
                                  partial=True)
    db.session.add(citizen)
    db.session.commit()

    citizen = citizen_schema.dump(citizen)

    return dict(data=citizen), 200


@imports.route("/<int:import_id>/citizens", methods=("GET",))
def get_citizens(import_id):
    import_ = Import.query.get(import_id)
    citizens = citizens_schema.dump(import_.citizens)
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

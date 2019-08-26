from flask import (abort,
                   Blueprint,
                   request, )

from ext import db
from models import (Import,
                    citizen_schema,
                    citizens_schema,
                    import_schema, )

imports = Blueprint("imports", __name__, url_prefix="/imports")


@imports.route("", methods=("POST",))
def post():
    try:
        import_ = import_schema.load(request.get_json())
        db.session.add(import_)
        db.session.commit()

        import_id = import_.import_id

        return dict(data=dict(import_id=import_id)), 201
    except Exception as err:
        db.session.rollback()
        abort(400, description=err)


@imports.route("/<int:import_id>/citizens/<int:citizen_id>", methods=("PATCH",))
def patch_citizens(import_id, citizen_id):
    try:
        import_ = Import.get(import_id)

        citizen = import_.get_citizen(citizen_id)
        citizen.remove_relationship()
        citizen_schema.context["import"] = import_
        citizen = citizen_schema.load(request.get_json(),
                                      instance=citizen,
                                      partial=True)
        citizen.ensure_relationship()

        db.session.add(citizen)
        db.session.commit()

        citizen = citizen_schema.dump(citizen)

        return dict(data=citizen), 200
    except Exception as err:
        db.session.rollback()
        abort(400, description=err)


@imports.route("/<int:import_id>/citizens", methods=("GET",))
def get_citizens(import_id):
    try:
        import_ = Import.get(import_id)
        citizens = citizens_schema.dump(import_.citizens)

        return dict(data=citizens), 200
    except Exception as err:
        db.session.rollback()
        abort(400, description=err)


@imports.route("/<int:import_id>/citizens/birthdays", methods=("GET",))
def get_citizens_birthdays(import_id):
    try:
        import_ = Import.get(import_id)
        birthdays = import_.get_birthdays()

        return dict(data=birthdays), 200
    except Exception as err:
        db.session.rollback()
        abort(400, description=err)


@imports.route("/<int:import_id>/towns/stat/percentile/age", methods=("GET",))
def get_towns_stat_percentile_age(import_id):
    try:
        import_ = Import.get(import_id)
        stats = import_.get_stats()

        return dict(data=stats), 200
    except Exception as err:
        db.session.rollback()
        abort(400, description=err)

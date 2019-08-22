from ext import (db,
                 ma, )


class Citizen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    import_id = db.Column(db.Integer, db.ForeignKey("import.import_id"))
    citizen_id = db.Column(db.Integer)
    town = db.Column(db.String)
    street = db.Column(db.String)
    building = db.Column(db.String)
    apartment = db.Column(db.Integer)
    name = db.Column(db.String)
    birth_date = db.Column(db.String)
    gender = db.Column(db.String)
    relative_id = db.Column(db.Integer, db.ForeignKey("citizen.id"))
    relatives = db.relationship("Citizen")

    def __repr__(self):
        return f"Citizen({self.citizen_id})"


class Import(db.Model):
    import_id = db.Column(db.Integer, primary_key=True)
    citizens = db.relationship("Citizen")

    def __repr__(self):
        return f"Import({self.import_id})"


class CitizenSchema(ma.ModelSchema):
    relatives = ma.Pluck("self", "citizen_id", many=True)

    class Meta:
        exclude = ("id",)
        model = Citizen
        sqla_session = db.session


class ImportSchema(ma.ModelSchema):
    citizens = ma.Nested(CitizenSchema, many=True)

    class Meta:
        model = Import
        sqla_session = db.session


citizen_schema = CitizenSchema()
citizens_schema = CitizenSchema(many=True)
import_schema = ImportSchema()

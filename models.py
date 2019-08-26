from datetime import datetime

from dateutil.relativedelta import relativedelta
from marshmallow import (pre_load,
                         post_load,
                         validate, )
from numpy import percentile

from ext import (db,
                 ma, )

relationship = db.Table("relationship",
                        db.Column("citizen_id", db.ForeignKey("citizen.id"), primary_key=True),
                        db.Column("relative_id", db.ForeignKey("citizen.id"), primary_key=True))


class Citizen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    import_id = db.Column(db.Integer, db.ForeignKey("import.import_id"))
    citizen_id = db.Column(db.Integer)
    town = db.Column(db.String)
    street = db.Column(db.String)
    building = db.Column(db.String)
    apartment = db.Column(db.Integer)
    name = db.Column(db.String)
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String)
    # Many-To-Many relationship
    relatives = db.relationship("Citizen", secondary=relationship, primaryjoin=(id == relationship.c.citizen_id),
                                secondaryjoin=(id == relationship.c.relative_id), lazy="dynamic")

    def get_age(self):
        return relativedelta(datetime.now(), self.birth_date).years

    def ensure_relationship(self):
        # self.relatives = [getattr(self, "import").get_citizen(relative.citizen_id)
        #                   for relative in self.relatives]
        for relative in self.relatives:
            if self not in relative.relatives:
                relative.relatives.append(self)

    def remove_relationship(self):
        for relative in self.relatives:
            if self in relative.relatives:
                relative.relatives.remove(self)

    def __repr__(self):
        return f"Citizen({self.citizen_id}, import_id={self.import_id}, id={self.id})"


class Import(db.Model):
    import_id = db.Column(db.Integer, primary_key=True)
    citizens = db.relationship("Citizen", backref="import", lazy="dynamic")

    @classmethod
    def get(cls, import_id):
        return cls.query.get(import_id)

    def get_citizen(self, citizen_id):
        return self.citizens.filter_by(citizen_id=citizen_id).one()

    def get_birthdays(self):
        birthdays = {month + 1: [] for month in range(12)}

        for citizen in self.citizens:
            for month in birthdays:
                presents = citizen.relatives.filter(db.extract("month", Citizen.birth_date) == month).count()
                if presents == 0:
                    continue
                entry = dict(citizen_id=citizen.citizen_id,
                             presents=presents)
                birthdays[month].append(entry)

        return birthdays

    def get_stats(self):
        stats = []

        for citizen in self.citizens.distinct(Citizen.town):
            town = citizen.town
            birthdays = [citizen.get_age() for citizen in self.citizens.filter_by(town=town)]
            p50, p75, p99 = percentile(birthdays, (50, 75, 99,))
            entry = dict(town=town,
                         p50=p50,
                         p75=p75,
                         p99=p99)
            stats.append(entry)

        return stats

    def __repr__(self):
        return f"Import({self.import_id})"


class CitizenSchema(ma.ModelSchema):
    citizen_id = ma.Integer(required=True, validate=validate.Range(0))
    town = ma.String(required=True, validate=validate.Regexp(r"\w"))
    street = ma.String(required=True, validate=validate.Regexp(r"\w"))
    building = ma.String(required=True, validate=validate.Regexp(r"\w"))
    apartment = ma.Integer(required=True, validate=validate.Range(0))
    name = ma.String(required=True, validate=validate.Regexp(r"^\w+ \w+( \w+)?$"))
    gender = ma.String(required=True, validate=validate.OneOf(("male", "female",)))

    relatives = ma.Pluck("self", "citizen_id", many=True)
    _relatives = None

    @pre_load(pass_many=True)
    def pre_load(self, data, many, **kwargs):
        if not many:
            self._relatives = data.pop("relatives")
        return data

    @post_load(pass_many=True)
    def post_load(self, data, many, **kwargs):
        if not many:
            data["relatives"] = [self.context["import"].get_citizen(relative_id) for relative_id in
                                 self._relatives]

            self._relatives = None

        return data

    class Meta:
        dateformat = "%d.%m.%Y"
        exclude = ("id",)
        # include_fk = True
        model = Citizen
        sqla_session = db.session


class ImportSchema(ma.ModelSchema):
    citizens = ma.Nested(CitizenSchema, many=True)
    _relatives = None

    @pre_load
    def pre_load(self, data, **kwargs):
        self._relatives = {citizen["citizen_id"]: citizen.pop("relatives") for citizen in data["citizens"]}

        return data

    @post_load
    def post_load(self, data, **kwargs):
        # for citizen in data.citizens:
        #     self.session.add(citizen)

        citizens = {citizen.citizen_id: citizen for citizen in data.citizens}
        for citizen in data.citizens:
            relatives = self._relatives[citizen.citizen_id]
            citizen.relatives = [citizens[relative_id] for relative_id in relatives]
            # self.session.add(citizen)

        self._relatives = None

        return data

    class Meta:
        model = Import
        sqla_session = db.session


citizen_schema = CitizenSchema()
citizens_schema = CitizenSchema(many=True)
import_schema = ImportSchema()

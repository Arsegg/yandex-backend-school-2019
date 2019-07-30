from mongoengine import *


class Citizen(EmbeddedDocument):
    """TODO: make field verifiers"""
    citizen_id = IntField()
    town = StringField()
    street = StringField()
    building = StringField()
    appartement = IntField()
    name = StringField()
    birth_date = DateField()
    gender = StringField()
    relatives = ListField(IntField())


class Import(Document):
    """TODO: create import_id : ImportIdField"""
    citizens = EmbeddedDocumentListField(Citizen)

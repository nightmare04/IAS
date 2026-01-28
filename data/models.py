import datetime

from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase


db = SqliteExtDatabase('./data/database.db', pragmas={'foreign_keys': 1})

class BaseModel(Model):
    id = IntegerField(primary_key=True)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

class PlaneType(BaseModel):
    name = CharField(unique=True)

class Podrazd(BaseModel):
    name = CharField(unique=True)

class Spec(BaseModel):
    plane_type = ForeignKeyField(PlaneType)
    name = CharField(unique=True)

class Group(BaseModel):
    spec = ForeignKeyField(Spec)
    name = CharField(unique=True)

class PlaneSystem(BaseModel):
    plane_type = ForeignKeyField(PlaneType)
    name = CharField(unique=True)
    group = ForeignKeyField(Group)

class Agregate(BaseModel):
    system = ForeignKeyField(PlaneSystem)
    count_on_plane = IntegerField(default=1)
    name = CharField(unique=False)

class Plane(BaseModel):
    plane_type = ForeignKeyField(PlaneType)
    podrazd = ForeignKeyField(Podrazd)
    number = CharField(unique=True)
    bort_number = CharField(unique=True)
    date_of_birth = DateField()

class OtkazAgregate(BaseModel):
    agregate = ForeignKeyField(Agregate)
    plane = ForeignKeyField(Plane)
    number = CharField()

class OtsutAgregate(BaseModel):
    agregate = ForeignKeyField(Agregate)
    plane = ForeignKeyField(Plane)
    number = CharField()


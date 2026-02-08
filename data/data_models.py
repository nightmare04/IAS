import datetime

from peewee import *


db = SqliteDatabase('./data/database.db', pragmas={'foreign_keys': 1})


class BaseModel(Model):
    id = IntegerField(primary_key=True)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


class PlaneTypeBase(BaseModel):
    name = CharField(unique=True)


class PodrazdBase(BaseModel):
    name = CharField(unique=True)


class GroupBase(BaseModel):
    plane_type = ForeignKeyField(PlaneTypeBase)
    name = CharField(unique=True)


class PlaneSystemBase(BaseModel):
    plane_type = ForeignKeyField(PlaneTypeBase)
    name = CharField(unique=True)
    group = ForeignKeyField(GroupBase)


class AgregateBase(BaseModel):
    system = ForeignKeyField(PlaneSystemBase)
    count_on_plane = IntegerField(default=1)
    name = CharField(unique=False)


class PlaneBase(BaseModel):
    plane_type = ForeignKeyField(PlaneTypeBase)
    podrazd = ForeignKeyField(PodrazdBase)
    zav_num = CharField(unique=True)
    bort_number = CharField(unique=False)


class OsobPlaneTypeBase(BaseModel):
    plane_type = ForeignKeyField(PlaneTypeBase)
    name = CharField(unique=True)


class OsobPlane(BaseModel):
    plane = ForeignKeyField(PlaneBase)
    osob = ForeignKeyField(OsobPlaneTypeBase)


class OtkazAgregateBase(BaseModel):
    agregate = ForeignKeyField(AgregateBase)
    plane = ForeignKeyField(PlaneBase)
    description = CharField(unique=False, default='')
    number = CharField()
    removed = BooleanField(default=False)



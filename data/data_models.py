import datetime

from peewee import *


db = SqliteDatabase('./data/database.db', pragmas={'foreign_keys': 1})

def get_systems_for_plane(plane:PlaneBase) -> list[PlaneSystemBase]:
    osob_list = OsobPlaneBase.select().where(OsobPlaneBase.plane == plane)
    systems = (PlaneSystemBase.select(PlaneSystemBase.id)
               .where(PlaneSystemBase.id.not_in(OsobSystemAddBase
                      .select(OsobSystemAddBase.system)))
               .where(PlaneSystemBase.id.not_in(OsobSystemRemoveBase
                      .select(OsobSystemRemoveBase.system)
                      .where(OsobSystemRemoveBase.osob << osob_list)))
               .union(OsobSystemAddBase
                      .select(OsobSystemAddBase.system)
                      .where(OsobSystemAddBase.osob << osob_list))
                    )
    return systems

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


class OsobBase(BaseModel):
    plane_type = ForeignKeyField(PlaneTypeBase)
    name = CharField(unique=True)


class OsobPlaneBase(BaseModel):
    osob = ForeignKeyField(OsobBase)
    plane = ForeignKeyField(PlaneBase)


class OsobSystemAddBase(BaseModel):
    osob = ForeignKeyField(OsobBase)
    system = ForeignKeyField(PlaneSystemBase)


class OsobSystemRemoveBase(BaseModel):
    osob = ForeignKeyField(OsobBase)
    system = ForeignKeyField(PlaneSystemBase)


class OtkazAgregateBase(BaseModel):
    agregate = ForeignKeyField(AgregateBase)
    plane = ForeignKeyField(PlaneBase)
    description = CharField(unique=False, default='')
    number = CharField()
    removed = BooleanField(default=False)



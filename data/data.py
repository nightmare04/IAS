import datetime

from peewee import *


db = SqliteDatabase('./data/database.db', pragmas={'foreign_keys': 1})

def get_systems_for_plane(plane:PlaneBase, group:GroupBase=None) -> list[PlaneSystemBase]:
    osob_list = OsobPlaneBase.select().where(OsobPlaneBase.plane == plane)
    systems = (PlaneSystemBase
               .select()
               .where(PlaneSystemBase.group == group)
               .where(PlaneSystemBase.id.not_in(OsobSystemAddBase
                                                .select(OsobSystemAddBase.system)
                                                .where(OsobSystemAddBase.system.plane_type == plane.id)))
               .where(PlaneSystemBase.id.not_in(OsobSystemRemoveBase
                                                .select(OsobSystemRemoveBase.system)
                                                .where(OsobSystemRemoveBase.osob << osob_list)))
               .switch(PlaneSystemBase)
               .union(PlaneSystemBase
                      .select()
                      .join(OsobSystemAddBase)
                      .where(OsobSystemAddBase.system.group == group.id)
                      .where(OsobSystemAddBase.osob << osob_list))
               )
    if group:
        systems = systems.where(PlaneSystemBase.group == group)
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
    plane_type = ForeignKeyField(PlaneTypeBase, backref='groups')
    name = CharField(unique=True)


class PlaneSystemBase(BaseModel):
    plane_type = ForeignKeyField(PlaneTypeBase, backref='systems')
    name = CharField(unique=True)
    group = ForeignKeyField(GroupBase)


class AgregateBase(BaseModel):
    system = ForeignKeyField(PlaneSystemBase, backref='agregates')
    count_on_plane = IntegerField(default=1)
    name = CharField(unique=False)


class PlaneBase(BaseModel):
    plane_type = ForeignKeyField(PlaneTypeBase, backref='planes')
    podrazd = ForeignKeyField(PodrazdBase, backref='planes')
    zav_num = CharField(unique=True)
    bort_number = CharField(unique=False)


class OsobBase(BaseModel):
    plane_type = ForeignKeyField(PlaneTypeBase, backref='osobs')
    name = CharField(unique=True)


class OsobPlaneBase(BaseModel):
    osob = ForeignKeyField(OsobBase, backref='osobs')
    plane = ForeignKeyField(PlaneBase)


class OsobSystemAddBase(BaseModel):
    osob = ForeignKeyField(OsobBase, backref='systems_to_add')
    system = ForeignKeyField(PlaneSystemBase, backref='systems_to_add')


class OsobSystemRemoveBase(BaseModel):
    osob = ForeignKeyField(OsobBase, backref='systems_to_remove')
    system = ForeignKeyField(PlaneSystemBase, backref='systems_to_remove')


class OtkazAgregateBase(BaseModel):
    agregate = ForeignKeyField(AgregateBase, backref='otkaz_agregates')
    plane = ForeignKeyField(PlaneBase , backref='otkaz_agregates')
    description = CharField(unique=False, default='')
    number = CharField()
    removed = BooleanField(default=False)



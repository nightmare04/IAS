import datetime

from peewee import *

db = SqliteDatabase('./data/database.db', pragmas={'foreign_keys': 1})


def get_systems_for_plane(plane: PlaneBase, group: GroupBase = None) -> list[SystemBase]:
    osob_list = OsobPlaneBase.select().where(OsobPlaneBase.plane == plane)
    systems = (SystemBase
               .select()
               .where(SystemBase.group == group)
               .where(SystemBase.id.not_in(OsobSystemAddBase
                                           .select(OsobSystemAddBase.system)
                                           .where(OsobSystemAddBase.system.plane_type == plane.id)))
               .where(SystemBase.id.not_in(OsobSystemRemoveBase
                                           .select(OsobSystemRemoveBase.system)
                                           .where(OsobSystemRemoveBase.osob << osob_list)))
               .switch(SystemBase)
               .union(SystemBase
                      .select()
                      .join(OsobSystemAddBase)
                      .where(OsobSystemAddBase.system.group == group.id)
                      .where(OsobSystemAddBase.osob << osob_list))
               )
    if group:
        systems = systems.where(SystemBase.group == group)
    return systems


def get_agregates_for_plane(plane: PlaneBase, system: SystemBase = None) -> list[AgregateBase]:
    osob_list = OsobPlaneBase.select().where(OsobPlaneBase.plane == plane)
    agregates = (AgregateBase
                 .select()
                 .where(AgregateBase.system.plane_type == plane.id)
                 .where(AgregateBase.id.not_in(OsobAgregateAddBase
                                               .select(OsobAgregateAddBase.agregate)
                                               .where(OsobAgregateAddBase.agregate.system.plane_type == plane.plane_type)))
                 .where(AgregateBase.id.not_in(OsobAgregateRemoveBase
                                               .select(OsobAgregateRemoveBase.agregate)
                                               .where(OsobAgregateRemoveBase.osob << osob_list)))
                 .switch(AgregateBase)
                 .union(AgregateBase
                        .select()
                        .join(OsobAgregateAddBase)
                        .where(OsobAgregateAddBase.agregate.system.plane_type == plane.plane_type)
                        .where(OsobAgregateAddBase.osob << osob_list)
                        )
                 )
    if system:
        agregates = agregates.where(AgregateBase.system == system)
    return agregates


class BaseModel(Model):
    id = IntegerField(primary_key=True)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


class TypeBase(BaseModel):
    name = CharField(unique=True)


class PodrazdBase(BaseModel):
    name = CharField(unique=True)


class GroupBase(BaseModel):
    plane_type = ForeignKeyField(TypeBase, backref='groups')
    name = CharField(unique=True)


class SystemBase(BaseModel):
    plane_type = ForeignKeyField(TypeBase, backref='systems')
    name = CharField(unique=True)
    group = ForeignKeyField(GroupBase)


class AgregateBase(BaseModel):
    system = ForeignKeyField(SystemBase, backref='agregates')
    count_on_plane = IntegerField(default=1)
    name = CharField(unique=False)


class PlaneBase(BaseModel):
    plane_type = ForeignKeyField(TypeBase, backref='planes')
    podrazd = ForeignKeyField(PodrazdBase, backref='planes')
    zav_num = CharField(unique=True)
    bort_number = CharField(unique=False)


class OsobBase(BaseModel):
    plane_type = ForeignKeyField(TypeBase, backref='osobs')
    name = CharField(unique=True)


class OsobPlaneBase(BaseModel):
    osob = ForeignKeyField(OsobBase, backref='osobs')
    plane = ForeignKeyField(PlaneBase)


class OsobSystemAddBase(BaseModel):
    osob = ForeignKeyField(OsobBase, backref='systems_to_add')
    system = ForeignKeyField(SystemBase)


class OsobSystemRemoveBase(BaseModel):
    osob = ForeignKeyField(OsobBase, backref='systems_to_remove')
    system = ForeignKeyField(SystemBase)


class OsobAgregateAddBase(BaseModel):
    osob = ForeignKeyField(OsobBase, backref='agregates_to_add')
    agregate = ForeignKeyField(AgregateBase)


class OsobAgregateRemoveBase(BaseModel):
    osob = ForeignKeyField(OsobBase, backref='agregates_to_remove')
    agregate = ForeignKeyField(AgregateBase)


class OtkazAgregateBase(BaseModel):
    agregate = ForeignKeyField(AgregateBase, backref='otkaz_agregates')
    plane = ForeignKeyField(PlaneBase, backref='otkaz_agregates')
    description = CharField(unique=False, default='')
    number = CharField()
    removed = BooleanField(default=False)

"""Aircraft-related models."""
from peewee import CharField, ForeignKeyField, IntegerField

from app.models.base import BaseModel


class TypeBase(BaseModel):
    """Aircraft type model."""
    name = CharField(unique=True)

    class Meta:
        table_name = "type_base"
        indexes = (("name", True),)


class PodrazdBase(BaseModel):
    """Division/Unit model."""
    name = CharField(unique=True)

    class Meta:
        table_name = "podrazd_base"
        indexes = (("name", True),)


class GroupBase(BaseModel):
    """Maintenance group model."""
    plane_type = ForeignKeyField(TypeBase, backref="groups", on_delete="CASCADE")
    name = CharField(unique=True)

    class Meta:
        table_name = "group_base"
        indexes = (("name", True),)


class SystemBase(BaseModel):
    """Aircraft system model."""
    plane_type = ForeignKeyField(TypeBase, backref="systems", on_delete="CASCADE")
    name = CharField(unique=True)
    group = ForeignKeyField(GroupBase, backref="systems", on_delete="CASCADE")

    class Meta:
        table_name = "system_base"
        indexes = (("name", True),)


class AgregateBase(BaseModel):
    """Agregate/Unit model."""
    system = ForeignKeyField(SystemBase, backref="agregates", on_delete="CASCADE")
    count_on_plane = IntegerField(default=1)
    name = CharField()

    class Meta:
        table_name = "agregate_base"


class PlaneBase(BaseModel):
    """Aircraft model."""
    plane_type = ForeignKeyField(TypeBase, backref="planes", on_delete="CASCADE")
    podrazd = ForeignKeyField(PodrazdBase, backref="planes", on_delete="CASCADE")
    zav_num = CharField(unique=True)
    bort_number = CharField()

    class Meta:
        table_name = "plane_base"
        indexes = (("zav_num", True),)

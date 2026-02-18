"""Failure tracking models."""
from peewee import BooleanField, CharField, ForeignKeyField

from app.models.aircraft import AgregateBase, PlaneBase
from app.models.base import BaseModel


class OtkazAgregateBase(BaseModel):
    """Failed agregate/unit model."""
    agregate = ForeignKeyField(AgregateBase, backref="otkaz_agregates", on_delete="CASCADE")
    plane = ForeignKeyField(PlaneBase, backref="otkaz_agregates", on_delete="CASCADE")
    description = CharField(default="")
    number = CharField()
    removed = BooleanField(default=False)

    class Meta:
        table_name = "otkaz_agregate_base"

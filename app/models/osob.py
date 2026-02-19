"""Aircraft features (osobennosti) models."""
from typing import Any

from peewee import CharField, ForeignKeyField

from app.models.aircraft import AgregateBase, PlaneBase, SystemBase, TypeBase
from app.models.base import BaseModel


def get_available_systems_for_plane(plane: PlaneBase, group: Any | None = None) -> list[SystemBase]:
    """Get systems available for aircraft considering features."""
    # Get features for this aircraft
    aircraft_features = [
        op.osob for op in OsobPlaneBase.select().where(OsobPlaneBase.plane == plane)
    ]

    # Get systems to remove and add from features
    systems_to_remove = set()
    systems_to_add = set()

    for feature in aircraft_features:
        systems_to_remove.update(
            osr.system for osr in OsobSystemRemoveBase.select().where(OsobSystemRemoveBase.osob == feature)
        )
        systems_to_add.update(
            osa.system for osa in OsobSystemAddBase.select().where(OsobSystemAddBase.osob == feature)
        )

    # Get base systems for this aircraft type
    base_query = SystemBase.select()
    base_query = base_query.where(SystemBase.plane_type == plane.plane_type)

    if group:
        base_query = base_query.where(SystemBase.group == group)

    base_systems = set(base_query)

    # Apply modifications
    available_systems = (base_systems - systems_to_remove) | systems_to_add

    return list(available_systems)


def get_available_agregates_for_plane(plane: PlaneBase, system: SystemBase | None = None) -> list[AgregateBase]:
    """Get agregates available for aircraft considering features."""
    # Get features for this aircraft
    aircraft_features = [
        op.osob for op in OsobPlaneBase.select().where(OsobPlaneBase.plane == plane)
    ]

    # Get agregates to remove and add from features
    agregates_to_remove = set()
    agregates_to_add = set()

    for feature in aircraft_features:
        agregates_to_remove.update(
            oar.agregate for oar in OsobAgregateRemoveBase.select().where(OsobAgregateRemoveBase.osob == feature)
        )
        agregates_to_add.update(
            oaa.agregate for oaa in OsobAgregateAddBase.select().where(OsobAgregateAddBase.osob == feature)
        )

    # Get base agregates for this aircraft type
    base_query = AgregateBase.select().join(SystemBase, on=(AgregateBase.system == SystemBase.id))
    base_query = base_query.where(SystemBase.plane_type == plane.plane_type)

    if system:
        base_query = base_query.where(AgregateBase.system == system)

    base_agregates = set(base_query)

    # Apply modifications
    available_agregates = (base_agregates - agregates_to_remove) | agregates_to_add

    return list(available_agregates)


class OsobBase(BaseModel):
    """Feature model for aircraft types."""
    plane_type = ForeignKeyField(TypeBase, backref="osobs", on_delete="CASCADE")
    name = CharField(unique=True)

    class Meta:
        table_name = "osob_base"
        indexes = (("name", True),)


class OsobPlaneBase(BaseModel):
    """Link between feature and aircraft."""
    osob = ForeignKeyField(OsobBase, backref="osobs", on_delete="CASCADE")
    plane = ForeignKeyField(PlaneBase, on_delete="CASCADE")

    class Meta:
        table_name = "osob_plane_base"


class OsobSystemAddBase(BaseModel):
    """Systems to add for specific feature."""
    osob = ForeignKeyField(OsobBase, backref="systems_to_add", on_delete="CASCADE")
    system = ForeignKeyField(SystemBase, on_delete="CASCADE")

    class Meta:
        table_name = "osob_system_add_base"


class OsobSystemRemoveBase(BaseModel):
    """Systems to remove for specific feature."""
    osob = ForeignKeyField(OsobBase, backref="systems_to_remove", on_delete="CASCADE")
    system = ForeignKeyField(SystemBase, on_delete="CASCADE")

    class Meta:
        table_name = "osob_system_remove_base"


class OsobAgregateAddBase(BaseModel):
    """Aggregates to add for specific feature."""
    osob = ForeignKeyField(OsobBase, backref="agregates_to_add", on_delete="CASCADE")
    agregate = ForeignKeyField(AgregateBase, on_delete="CASCADE")

    class Meta:
        table_name = "osob_agregate_add_base"


class OsobAgregateRemoveBase(BaseModel):
    """Aggregates to remove for specific feature."""
    osob = ForeignKeyField(OsobBase, backref="agregates_to_remove", on_delete="CASCADE")
    agregate = ForeignKeyField(AgregateBase, on_delete="CASCADE")

    class Meta:
        table_name = "osob_agregate_remove_base"

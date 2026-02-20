"""
Legacy data module - backward compatibility.
Imports from data.models structure.
"""
from data.models import (
    TypeBase,
    PodrazdBase,
    GroupBase,
    SystemBase,
    AgregateBase,
    PlaneBase,
    OsobBase,
    OsobPlaneBase,
    OsobSystemAddBase,
    OsobSystemRemoveBase,
    OsobAgregateAddBase,
    OsobAgregateRemoveBase,
    OtkazAgregateBase,
)
from app.database import get_database

db = get_database()


def get_systems_for_plane(plane: PlaneBase, group: GroupBase = None) -> list[SystemBase]:
    """Get systems for aircraft with optional group filter."""
    osob_list = OsobPlaneBase.select().where(OsobPlaneBase.plane == plane)
    systems = (
        SystemBase.select()
        .where(SystemBase.group == group)
        .where(
            SystemBase.id.not_in(
                OsobSystemAddBase.select(OsobSystemAddBase.system).where(
                    OsobSystemAddBase.system.plane_type == plane.id
                )
            )
        )
        .where(
            SystemBase.id.not_in(
                OsobSystemRemoveBase.select(OsobSystemRemoveBase.system).where(
                    OsobSystemRemoveBase.osob << osob_list
                )
            )
        )
        .switch(SystemBase)
        .union(
            SystemBase.select()
            .join(OsobSystemAddBase)
            .where(OsobSystemAddBase.system.group == group.id)
            .where(OsobSystemAddBase.osob << osob_list)
        )
    )
    if group:
        systems = systems.where(SystemBase.group == group)
    return list(systems)


def get_agregates_for_plane(plane: PlaneBase, system: SystemBase = None) -> list[AgregateBase]:
    """Get agregates for aircraft with optional system filter."""
    osob_list = OsobPlaneBase.select().where(OsobPlaneBase.plane == plane)
    agregates = (
        AgregateBase.select()
        .where(AgregateBase.system.plane_type == plane.plane_type)
        .where(
            AgregateBase.id.not_in(
                OsobAgregateAddBase.select(OsobAgregateAddBase.agregate).where(
                    OsobAgregateAddBase.agregate.system.plane_type == plane.plane_type
                )
            )
        )
        .where(
            AgregateBase.id.not_in(
                OsobAgregateRemoveBase.select(OsobAgregateRemoveBase.agregate).where(
                    OsobAgregateRemoveBase.osob << osob_list
                )
            )
        )
        .switch(AgregateBase)
        .union(
            AgregateBase.select()
            .join(OsobAgregateAddBase)
            .where(OsobAgregateAddBase.agregate.system.plane_type == plane.plane_type)
            .where(OsobAgregateAddBase.osob << osob_list)
        )
    )
    if system:
        agregates = agregates.where(AgregateBase.system == system)
    return list(agregates)


__all__ = [
    "db",
    "TypeBase",
    "PodrazdBase",
    "GroupBase",
    "SystemBase",
    "AgregateBase",
    "PlaneBase",
    "OsobBase",
    "OsobPlaneBase",
    "OsobSystemAddBase",
    "OsobSystemRemoveBase",
    "OsobAgregateAddBase",
    "OsobAgregateRemoveBase",
    "OtkazAgregateBase",
    "get_systems_for_plane",
    "get_agregates_for_plane",
]

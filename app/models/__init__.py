"""Peewee models for IAS application."""
from app.models.aircraft import (
    AgregateBase,
    GroupBase,
    PlaneBase,
    PodrazdBase,
    SystemBase,
    TypeBase,
)
from app.models.base import BaseModel, db
from app.models.failures import OtkazAgregateBase
from app.models.osob import (
    OsobAgregateAddBase,
    OsobAgregateRemoveBase,
    OsobBase,
    OsobPlaneBase,
    OsobSystemAddBase,
    OsobSystemRemoveBase,
)

__all__ = [
    "db",
    "BaseModel",
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
]

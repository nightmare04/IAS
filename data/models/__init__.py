"""Peewee models for IAS application."""
from .aircraft import (
    AgregateBase,
    GroupBase,
    PlaneBase,
    PodrazdBase,
    SystemBase,
    TypeBase,
)
from .base import BaseModel, db
from .failures import OtkazAgregateBase
from .osob import (
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

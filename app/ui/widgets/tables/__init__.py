"""Tables package for IAS application."""
from .agregate import AgregateTable
from .base import UnTableView
from .group import GroupTable
from .ispravnost import IspravnostTable
from .osob import OsobTable
from .plane_types import PlaneTypesTable
from .planes import PlanesTable
from .podrazd import PodrazdTable
from .system import SystemTable

__all__ = [
    "UnTableView",
    "IspravnostTable",
    "PlaneTypesTable",
    "PodrazdTable",
    "GroupTable",
    "SystemTable",
    "AgregateTable",
    "PlanesTable",
    "OsobTable",
]

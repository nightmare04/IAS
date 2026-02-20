"""Table views and models for IAS application."""
from app.ui.widgets.tables.agregate import AgregateModel, AgregateTable
from app.ui.widgets.tables.base import UnTableModel, UnTableView
from app.ui.widgets.tables.group import GroupModel, GroupTable
from app.ui.widgets.tables.ispravnost import IspravnostTable, IspravnostTableModel
from app.ui.widgets.tables.osob import OsobModel, OsobTable
from app.ui.widgets.tables.plane_types import PlanesTypesModel, PlaneTypesTable
from app.ui.widgets.tables.planes import PlanesModel, PlanesTable
from app.ui.widgets.tables.podrazd import PodrazdModel, PodrazdTable
from app.ui.widgets.tables.system import SystemModel, SystemTable

__all__ = [
    # Base
    "UnTableModel",
    "UnTableView",
    # Plane types
    "PlanesTypesModel",
    "PlaneTypesTable",
    # Divisions
    "PodrazdModel",
    "PodrazdTable",
    # Groups
    "GroupModel",
    "GroupTable",
    # Systems
    "SystemModel",
    "SystemTable",
    # Agregates
    "AgregateModel",
    "AgregateTable",
    # Planes
    "PlanesModel",
    "PlanesTable",
    # Osob
    "OsobModel",
    "OsobTable",
    # Ispravnost
    "IspravnostTableModel",
    "IspravnostTable",
]

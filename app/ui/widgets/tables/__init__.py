"""Table views and models for IAS application."""
from app.ui.widgets.tables.agregate_table import AgregateModel, AgregateTable
from app.ui.widgets.tables.base_table import UnTableModel, UnTableView
from app.ui.widgets.tables.group_table import GroupModel, GroupTable
from app.ui.widgets.tables.ispravnost_table import IspravnostTable, IspravnostTableModel
from app.ui.widgets.tables.osobs_table import OsobModel, OsobTable
from app.ui.widgets.tables.plane_types_table import PlanesTypesModel, PlaneTypesTable
from app.ui.widgets.tables.planes_table import PlanesModel, PlanesTable
from app.ui.widgets.tables.podrazd_table import PodrazdModel, PodrazdTable
from app.ui.widgets.tables.system_table import SystemModel, SystemTable

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

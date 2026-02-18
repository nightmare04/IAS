"""UI components package."""
from app.ui.widgets.buttons import IASButton, PlaneBtn
from app.ui.widgets.combo_box import (
    AgregateComboBox,
    ComboBoxModel,
    GroupComboBox,
    IASComboBox,
    PlaneTypeComboBox,
    PodrazdComboBox,
    SystemComboBox,
)
from app.ui.widgets.groups import PodrGroup
from app.ui.widgets.tables import (
    AgregateTable,
    GroupTable,
    IspravnostTable,
    OsobTable,
    PlanesTable,
    PlaneTypesTable,
    PodrazdTable,
    UnTableView,
)

__all__ = [
    "IASButton",
    "PlaneBtn",
    "IASComboBox",
    "ComboBoxModel",
    "PlaneTypeComboBox",
    "PodrazdComboBox",
    "GroupComboBox",
    "SystemComboBox",
    "AgregateComboBox",
    "UnTableView",
    "IspravnostTable",
    "PlaneTypesTable",
    "PodrazdTable",
    "GroupTable",
    "AgregateTable",
    "PlanesTable",
    "OsobTable",
    "PodrGroup",
]

"""Table view for aircraft types."""
from typing import Any

from app.ui.models.reference import PlanesTypesModel

from .base import UnTableView


class PlaneTypesTable(UnTableView):
    """Table view for aircraft types."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.table_model = PlanesTypesModel()
        self.setModel(self.table_model)

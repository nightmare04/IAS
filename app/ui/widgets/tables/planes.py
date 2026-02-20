"""Table view for aircraft."""
from typing import Any

from app.ui.models.reference import PlanesModel

from .base import UnTableView


class PlanesTable(UnTableView):
    """Table view for aircraft."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.table_model = PlanesModel()
        self.setModel(self.table_model)

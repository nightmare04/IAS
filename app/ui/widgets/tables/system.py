"""Table view for aircraft systems."""
from typing import Any

from app.ui.models.reference import SystemModel

from .base import UnTableView


class SystemTable(UnTableView):
    """Table view for aircraft systems."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.table_model = SystemModel()
        self.setModel(self.table_model)

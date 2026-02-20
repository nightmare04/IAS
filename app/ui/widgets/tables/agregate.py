"""Table view for aggregates/units."""
from typing import Any

from app.ui.models.reference import AgregateModel

from .base import UnTableView


class AgregateTable(UnTableView):
    """Table view for aggregates/units."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.table_model = AgregateModel()
        self.setModel(self.table_model)

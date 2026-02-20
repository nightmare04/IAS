"""Table view for maintenance groups."""
from typing import Any

from app.ui.models.reference import GroupModel

from .base import UnTableView


class GroupTable(UnTableView):
    """Table view for maintenance groups."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.table_model = GroupModel()
        self.setModel(self.table_model)

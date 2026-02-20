"""Table view for maintenance groups."""
from typing import Any

from data.models.aircraft import GroupBase, TypeBase

from .base import UnTableModel, UnTableView


class GroupModel(UnTableModel):
    """Table model for maintenance groups."""
    HEADERS: list[str] = [
        "Группа",
        "Тип"
    ]

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)

    def load_data(self, filter_str: str | None = None) -> None:
        """Load maintenance groups with optional filter."""
        self.beginResetModel()
        self.clear_data()
        query = GroupBase.select().join(TypeBase)
        if filter_str is not None:
            query = query.where(TypeBase.name == filter_str)
        for data in query:
            self._data.append([data, data.name, data.plane_type.name])
        self.endResetModel()


class GroupTable(UnTableView):
    """Table view for maintenance groups."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.table_model = GroupModel()
        self.setModel(self.table_model)

    def set_filter(self, plane_type: str):
        self.table_model.load_data(filter_str=plane_type)

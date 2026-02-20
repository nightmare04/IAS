"""Table view for aircraft systems."""
from typing import Any

from data.models.aircraft import GroupBase, SystemBase, TypeBase

from .base_table import UnTableModel, UnTableView


class SystemModel(UnTableModel):
    """Table model for aircraft systems."""
    HEADERS: list[str] = [
        "Система",
        "Группа обслуживания",
        "Тип самолета"
    ]

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)

    def load_data(self, filter: dict | None = None) -> None:
        """Load systems with optional filter."""
        self.beginResetModel()
        self.clear_data()
        query = SystemBase.select().join(GroupBase).join(TypeBase)
        if filter is not None:
            if isinstance(filter.get('plane_type'), TypeBase):
                query = query.where(SystemBase.plane_type == filter.get('plane_type'))
            if isinstance(filter.get('group'), GroupBase):
                query = query.where(SystemBase.group == filter.get('group'))
        for data in query:
            self._data.append([data, data.name, data.group.name, data.plane_type.name])
        self.endResetModel()


class SystemTable(UnTableView):
    """Table view for aircraft systems."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.table_model = SystemModel()
        self.setModel(self.table_model)

    def set_filter(self, filter: dict):
        self.table_model.load_data(filter=filter)

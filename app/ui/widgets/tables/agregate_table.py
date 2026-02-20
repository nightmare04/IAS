"""Table view for aggregates/units."""
from typing import Any

from data.models.aircraft import AgregateBase, GroupBase, SystemBase, TypeBase

from .base_table import UnTableModel, UnTableView


class AgregateModel(UnTableModel):
    """Table model for aggregates/units."""

    HEADERS: list[str] = [
        "Блок/Агрегат",
        "Система",
        "Группа",
        "Тип самолета"
    ]

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)

    def load_data(
        self,
        filter_type: Any | None = None,
        filter_group: Any | None = None,
        filter_system: Any | None = None,
    ) -> None:
        """Load aggregates with optional filters."""
        self.beginResetModel()
        query = (
            AgregateBase.select()
            .join(SystemBase)
            .join(GroupBase)
            .join(TypeBase)
        )

        if filter_system:
            query = query.where(AgregateBase.system == filter_system)
        elif filter_group:
            query = query.where(AgregateBase.system.group == filter_group)
        elif filter_type:
            query = query.where(AgregateBase.system.plane_type == filter_type)

        self.clear_data()
        for agregate in query:
            self._data.append(
                [
                    agregate,
                    agregate.name,
                    agregate.system.name,
                    agregate.system.group.name,
                    agregate.system.plane_type.name,
                ]
            )
        self.endResetModel()


class AgregateTable(UnTableView):
    """Table view for aggregates/units."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.table_model = AgregateModel()
        self.setModel(self.table_model)

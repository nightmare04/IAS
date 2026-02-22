"""Table view for aircraft features."""
from typing import Any

from data.models.osob import OsobBase

from .base_table import UnTableModel, UnTableView


class OsobModel(UnTableModel):
    """Table model for aircraft features."""

    HEADERS: list[str] = [
        "Тип самолета",
        "Особенности",
    ]

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)

    def load_data(self, filter_type: Any | None = None) -> None:
        """Load features with optional filter."""
        self.beginResetModel()
        self.clear_data()
        self._headers = ["Тип самолета", "Особенности"]
        if filter_type:
            query = OsobBase.select().where(OsobBase.plane_type == filter_type)
        else:
            query = OsobBase.select()

        for data in query:
            self._data.append([data, data.plane_type, data.name])
        self.endResetModel()


class OsobTable(UnTableView):
    """Table view for aircraft features."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.table_model = OsobModel()
        self.setModel(self.table_model)

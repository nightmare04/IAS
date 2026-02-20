"""Table view for divisions."""
from typing import Any

from data.models.aircraft import PodrazdBase

from .base_table import UnTableModel, UnTableView


class PodrazdModel(UnTableModel):
    """Table model for divisions."""
    HEADERS: list[str] = [
        "Наименование",
    ]

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)

    def load_data(self) -> None:
        """Load divisions."""
        self.beginResetModel()
        self.clear_data()
        query = PodrazdBase.select()
        for data in query:
            self._data.append([data, data.name])
        self.endResetModel()


class PodrazdTable(UnTableView):
    """Table view for divisions."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.table_model = PodrazdModel()
        self.setModel(self.table_model)

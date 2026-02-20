"""Table view for aircraft types."""
from typing import Any

from data.models.aircraft import TypeBase

from .base import UnTableModel, UnTableView


class PlanesTypesModel(UnTableModel):
    """Table model for aircraft types."""
    HEADERS: list[str] = [
        "Наименование",
    ]

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)

    def load_data(self) -> None:
        """Load aircraft types."""
        self.beginResetModel()
        self.clear_data()
        query = TypeBase.select()
        for plane_type in list(query):
            self._data.append([plane_type, plane_type.name])
        self.endResetModel()


class PlaneTypesTable(UnTableView):
    """Table view for aircraft types."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.table_model = PlanesTypesModel()
        self.setModel(self.table_model)

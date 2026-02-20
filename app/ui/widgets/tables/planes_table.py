"""Table view for aircraft."""
from typing import Any

from data.models.aircraft import PlaneBase, PodrazdBase, TypeBase

from .base_table import UnTableModel, UnTableView


class PlanesModel(UnTableModel):
    """Table model for aircraft."""

    HEADERS: list[str] = [
        "Тип самолета",
        "Подразделение",
        "Бортовой номер",
    ]

    def __init__(self, parent: Any | None = None) -> None:
        self.filter: dict[str, Any] = {}
        super().__init__(parent)

    def set_filter(self, filter_dict: dict[str, Any]) -> None:
        """Set filter for aircraft list."""
        self.filter = filter_dict
        self.load_data()

    def load_data(self) -> None:
        """Load aircraft with optional filters."""
        self.beginResetModel()
        self.clear_data()
        query = PlaneBase.select()

        if isinstance(self.filter.get("plane_type"), TypeBase):
            query = query.where(PlaneBase.plane_type == self.filter["plane_type"])

        if isinstance(self.filter.get("podrazd"), PodrazdBase):
            query = query.where(PlaneBase.podrazd == self.filter["podrazd"])

        for data in query:
            self._data.append(
                [data, data.plane_type.name, data.podrazd.name, data.bort_number]
            )
        self.endResetModel()


class PlanesTable(UnTableView):
    """Table view for aircraft."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.table_model = PlanesModel()
        self.setModel(self.table_model)

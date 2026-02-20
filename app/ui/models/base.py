"""Base table models for IAS application."""
from typing import Any

from PyQt6.QtCore import QAbstractTableModel, Qt


class TableModel(QAbstractTableModel):
    """Base model for database-backed tables."""

    HEADERS: list[str] = []

    def __init__(self, data_model, parent=None, **kwargs) -> None:
        super().__init__(parent)
        self.data_model = data_model
        self.filter_args = {}
        self.filter_args.update(kwargs)
        self._data = data_model.select()

    def _filter_data(self):
        if self.filter_args.get('plane_type') is not None:
            self._data = self._data.where(self.data_model.plane_type == self.filter_args.get('plane_type'))


class UnTableModel(QAbstractTableModel):
    """Base table model with common functionality."""

    HEADERS: list[str] = []

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self._data: list[list[Any]] = []
        self.load_data()

    def load_data(self) -> None:
        """Load data from database. Override in subclasses."""
        pass

    def rowCount(self, parent: Any | None = None) -> int:
        """Return number of rows."""
        return len(self._data)

    def columnCount(self, parent: Any | None = None) -> int:
        """Return number of columns."""
        return len(self.HEADERS)

    def data(self, index: Any, role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole) -> Any:
        """Return data for the given index and role."""
        if not index.isValid():
            return None
        row = index.row()
        col = index.column()

        if 0 <= row < self.rowCount() and 0 <= col < self.columnCount():
            if role == Qt.ItemDataRole.DisplayRole:
                return self._data[row][col + 1]
            elif role == Qt.ItemDataRole.UserRole:
                return self._data[row][0]
        return None

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole
    ) -> Any:
        """Return header data."""
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]
        return None

    def clear_data(self) -> None:
        """Clear all data."""
        self._data = []

    @staticmethod
    def delete_item(item: Any) -> None:
        """Delete item from database."""
        item.delete_instance()

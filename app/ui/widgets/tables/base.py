"""Base table view for IAS application."""
from typing import Any

from PyQt6.QtCore import QAbstractTableModel, Qt, pyqtSignal
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QAbstractItemView, QHeaderView, QMenu, QSizePolicy, QTableView


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


class UnTableView(QTableView):
    """Base table view with context menu support."""

    edit_signal = pyqtSignal(object)
    delete_signal = pyqtSignal(object)

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.table_model = UnTableModel()
        self.setAlternatingRowColors(False)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)  # type: ignore
        header.setStretchLastSection(True)  # type: ignore

    def show_context_menu(self, position: Any) -> None:
        """Show context menu at position."""
        index = self.indexAt(position)
        model = self.model()

        menu = QMenu(self)

        if index.isValid():
            item = model.data(index, role=Qt.ItemDataRole.UserRole)  # type: ignore
            edit_action = QAction("✏️ Изменить элемент", self)
            edit_action.triggered.connect(lambda checked: self.edit_item(item))
            menu.addAction(edit_action)
            delete_action = QAction("🗑️ Удалить элемент", self)
            delete_action.triggered.connect(lambda checked: self.delete_item(item))
            menu.addAction(delete_action)

        menu.exec(self.viewport().mapToGlobal(position))  # type: ignore

    def edit_item(self, item: Any) -> None:
        """Emit edit signal with item."""
        self.edit_signal.emit(item)

    def delete_item(self, item: Any) -> None:
        """Emit delete signal with item."""
        self.delete_signal.emit(item)

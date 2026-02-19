"""Custom table views for IAS application."""
from typing import Any

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QAbstractItemView, QHeaderView, QMenu, QSizePolicy, QTableView

from app.models.aircraft import PlaneBase
from app.ui.models.tables import (
    AgregateModel,
    GroupModel,
    IspravnostTableModel,
    OsobModel,
    PlanesModel,
    PlanesTypesModel,
    PodrazdModel,
    SystemModel,
    UnTableModel,
)


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
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents) # type: ignore
        header.setStretchLastSection(True) # type: ignore

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

        menu.exec(self.viewport().mapToGlobal(position)) # type: ignore

    def edit_item(self, item: Any) -> None:
        """Emit edit signal with item."""
        self.edit_signal.emit(item)

    def delete_item(self, item: Any) -> None:
        """Emit delete signal with item."""
        self.delete_signal.emit(item)


class IspravnostTable(UnTableView):
    """Table view for aircraft serviceability data."""

    def __init__(self, plane: PlaneBase, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.table_model = IspravnostTableModel(plane)
        self.setModel(self.table_model)

    def set_span_for_groups(self) -> None:
        """Set row spans for group rows."""
        self.clear_all_span()
        if isinstance(self.table_model, IspravnostTableModel):
            for row in range(self.table_model.rowCount()):
                if self.table_model.get_row_type(row) == 'group':
                    self.setSpan(row, 0, 1, self.table_model.columnCount())

    def clear_all_span(self) -> None:
        """Clear all row spans."""
        if isinstance(self.table_model, IspravnostTableModel):
            rows = self.table_model.rowCount()
            cols = self.table_model.columnCount()
            for row in range(rows):
                for col in range(cols):
                    if self.rowSpan(row, col) > 1:
                        self.setSpan(row, col, 1, 1)

    def set_filter(self, filter_text: str) -> None:
        """Set filter for table data."""
        pass

    def load_data(self) -> None:
        """Load data from database."""
        self.table_model.load_data()
        self.clear_all_span()
        QTimer.singleShot(0, self.set_span_for_groups)


class PlaneTypesTable(UnTableView):
    """Table view for aircraft types."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.table_model = PlanesTypesModel()
        self.setModel(self.table_model)


class PodrazdTable(UnTableView):
    """Table view for divisions."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.table_model = PodrazdModel()
        self.setModel(self.table_model)


class GroupTable(UnTableView):
    """Table view for maintenance groups."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.table_model = GroupModel()
        self.setModel(self.table_model)

class SystemTable(UnTableView):
    """Table view for aircraft systems."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.table_model = SystemModel()
        self.setModel(self.table_model)


class AgregateTable(UnTableView):
    """Table view for aggregates/units."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.table_model = AgregateModel()
        self.setModel(self.table_model)


class PlanesTable(UnTableView):
    """Table view for aircraft."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.table_model = PlanesModel()
        self.setModel(self.table_model)

class OsobTable(UnTableView):
    """Table view for aircraft features."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.table_model = OsobModel()
        self.setModel(self.table_model)

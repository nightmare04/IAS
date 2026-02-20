"""Base table view for IAS application."""
from typing import Any

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QAbstractItemView, QHeaderView, QMenu, QSizePolicy, QTableView

from app.ui.models import (
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

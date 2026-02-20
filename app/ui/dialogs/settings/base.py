"""Base classes for settings dialogs."""

from typing import Any

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)


class UnDialog(QDialog):
    """Base dialog for viewing and editing reference data."""

    updated = pyqtSignal()

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.setGeometry(300, 300, 400, 300)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Buttons
        self.btn_ok = QPushButton("OK")
        self.btn_ok.clicked.connect(self.accept)
        self.btn_add = QPushButton("Добавить")
        self.btn_add.clicked.connect(self.add_item)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.btn_ok)
        self.button_layout.addWidget(self.btn_add)

    def setup_ui(self, table_class: type, table_kwargs: dict | None = None) -> None:
        """Initialize table and connect signals."""
        self.table = table_class(**(table_kwargs or {}))
        self.table.edit_signal.connect(self.edit_item)
        self.table.delete_signal.connect(self.delete_item)
        self.main_layout.insertWidget(0, self.table)
        self.main_layout.addLayout(self.button_layout)

    def add_item(self) -> None:
        """Override in subclasses."""
        raise NotImplementedError()

    def edit_item(self, item: Any) -> None:
        """Override in subclasses."""
        raise NotImplementedError()

    def delete_item(self, item: Any) -> None:
        """Override in subclasses."""
        raise NotImplementedError()

    def refresh_data(self, **kwargs: Any) -> None:
        """Refresh table data."""
        if hasattr(self.table, "table_model"):
            self.table.table_model.load_data(**kwargs)

    def handle_dialog(
        self, dialog_class: type, method: str = "add", item: Any | None = None, **dialog_kwargs: Any
    ) -> QDialog | None:
        """Common method for opening add/edit dialogs."""
        dialog = dialog_class(self)
        dialog.updated.connect(self.refresh_data)

        if method == "add":
            dialog.add_dialog(**dialog_kwargs)
        else:
            dialog.edit_dialog(item)

        if dialog.exec():
            self.updated.emit()
            return dialog
        return None


class UnAddEditDialog(QDialog):
    """Base dialog for adding/editing reference data items."""

    updated = pyqtSignal()

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.item: Any | None = None
        self.setModal(True)
        self.setFixedWidth(400)
        self.main_layout = QVBoxLayout()
        self.form_layout = QFormLayout()
        self.button_layout = QHBoxLayout()

        self.btn_ok = QPushButton("Добавить")
        self.btn_ok.clicked.connect(self.add_or_save_item)
        self.btn_cancel = QPushButton("Отменить")
        self.btn_cancel.clicked.connect(self.reject)

        self.button_layout.addWidget(self.btn_ok)
        self.button_layout.addWidget(self.btn_cancel)

        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addLayout(self.button_layout)
        self.setLayout(self.main_layout)

    def add_or_save_item(self) -> None:
        """Override in subclasses."""
        raise NotImplementedError

    def add_dialog(self, **kwargs: Any) -> None:
        """Called when opening in add mode."""
        pass

    def edit_dialog(self, item: Any) -> None:
        """Called when opening in edit mode."""
        self.item = item
        self.btn_ok.setText("Сохранить")

    def show_error(self, message: str) -> None:
        """Show error message."""
        QMessageBox.warning(self, "Ошибка", message)


class SingleFieldMixin:
    """Mixin for dialogs with single text input field."""

    def __init__(self, field_label: str, parent: Any | None = None) -> None:
        self.field_label = field_label
        super().__init__()

    def init_field(self) -> None:
        """Initialize text input field."""
        self.field_edit = QLineEdit()
        self.form_layout.addRow(self.field_label, self.field_edit)  # type: ignore

    def set_field_text(self, text: str) -> None:
        """Set field text."""
        self.field_edit.setText(text)

    def get_field_text(self) -> str:
        """Get field text."""
        return self.field_edit.text().strip()

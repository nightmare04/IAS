"""Dialogs for managing maintenance groups."""

from typing import Any

from PyQt6.QtWidgets import QLineEdit

from data.models.aircraft import GroupBase, TypeBase
from app.ui.dialogs.settings.base import UnAddEditDialog, UnDialog
from app.ui.widgets.combo_box import PlaneTypeComboBox
from app.ui.widgets.tables import GroupTable


class SettingsGroup(UnDialog):
    """Dialog for managing maintenance groups."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Группы обслуживания")

        self.type_combo = PlaneTypeComboBox()

        self.setup_ui(GroupTable, {"parent": self})
        self.main_layout.insertWidget(0, self.type_combo)

    def add_item(self) -> None:
        selected_type = self.type_combo.currentData()
        self.handle_dialog(AddGroup, "add", plane_type=selected_type if selected_type else None)

    def edit_item(self, item: Any) -> None:
        self.handle_dialog(AddGroup, "edit", item)

    def delete_item(self, item: Any) -> None:
        self.table.table_model.delete_item(item)
        self.refresh_data()
        self.updated.emit()


class AddGroup(UnAddEditDialog):
    """Dialog for adding/editing maintenance group."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Группы обслуживания")

        self.type_combo = PlaneTypeComboBox()
        self.group_edit = QLineEdit()

        self.form_layout.addRow("Тип самолета", self.type_combo)
        self.form_layout.addRow("Название группы", self.group_edit)

    def add_dialog(self, plane_type: TypeBase | None = None) -> None:
        if plane_type and isinstance(plane_type, TypeBase):
            self.type_combo.setCurrentText(str(plane_type.name))

    def edit_dialog(self, item: Any) -> None:
        super().edit_dialog(item)
        self.type_combo.setCurrentText(item.plane_type.name)
        self.group_edit.setText(item.name)

    def add_or_save_item(self) -> None:
        name = self.group_edit.text().strip()
        plane_type = self.type_combo.currentData()

        if not name:
            self.show_error("Название группы не может быть пустым")
            return

        if plane_type is None:
            self.show_error("Выберите тип самолета")
            return

        if self.item:
            self.item.name = name
            self.item.plane_type = plane_type
            self.item.save()
        else:
            GroupBase.create(name=name, plane_type=plane_type)

        self.updated.emit()
        self.accept()

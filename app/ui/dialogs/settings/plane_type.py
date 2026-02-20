"""Dialogs for managing aircraft types."""

from typing import Any

from data.models.aircraft import TypeBase
from app.ui.dialogs.settings.base import SingleFieldMixin, UnAddEditDialog, UnDialog
from app.ui.widgets.tables import PlaneTypesTable


class SettingsPlaneType(UnDialog):
    """Dialog for managing aircraft types."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Типы самолетов")
        self.setup_ui(PlaneTypesTable)

    def add_item(self) -> None:
        self.handle_dialog(AddPlaneType, "add")

    def edit_item(self, item: Any) -> None:
        self.handle_dialog(AddPlaneType, "edit", item)

    def delete_item(self, item: Any) -> None:
        self.table.table_model.delete_item(item)
        self.refresh_data()
        self.updated.emit()


class AddPlaneType(SingleFieldMixin, UnAddEditDialog):
    """Dialog for adding/editing aircraft type."""

    def __init__(self, parent: Any | None = None) -> None:
        SingleFieldMixin.__init__(self, "Тип самолета:", parent)
        self.init_field()
        self.setWindowTitle("Добавить тип самолета")

    def edit_dialog(self, item: Any) -> None:
        super().edit_dialog(item)
        self.set_field_text(item.name)

    def add_or_save_item(self) -> None:
        name = self.get_field_text()
        if not name:
            self.show_error("Название не может быть пустым")
            return

        if self.item:
            self.item.name = name
            self.item.save()
        else:
            TypeBase.create(name=name)

        self.updated.emit()
        self.accept()

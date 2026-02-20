"""Dialogs for managing divisions."""

from typing import Any

from app.models.aircraft import PodrazdBase
from app.ui.dialogs.settings.base import SingleFieldMixin, UnAddEditDialog, UnDialog
from app.ui.widgets.tables import PodrazdTable


class SettingsPodrazd(UnDialog):
    """Dialog for managing divisions."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Подразделения")
        self.setup_ui(PodrazdTable)

    def add_item(self) -> None:
        self.handle_dialog(AddPodrazd, "add")

    def edit_item(self, item: Any) -> None:
        self.handle_dialog(AddPodrazd, "edit", item)

    def delete_item(self, item: Any) -> None:
        self.table.table_model.delete_item(item)
        self.refresh_data()
        self.updated.emit()


class AddPodrazd(SingleFieldMixin, UnAddEditDialog):
    """Dialog for adding/editing division."""

    def __init__(self, parent: Any | None = None) -> None:
        SingleFieldMixin.__init__(self, "Название подразделения:", parent)
        self.init_field()
        self.setWindowTitle("Подразделение")

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
            PodrazdBase.create(name=name)

        self.updated.emit()
        self.accept()

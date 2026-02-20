"""Dialogs for managing aircraft features (osobennosti)."""

from typing import Any

from app.ui.dialogs.settings.base import UnDialog
from app.ui.widgets.combo_box import PlaneTypeComboBox
from app.ui.widgets.tables import OsobTable


class SettingsOsob(UnDialog):
    """Dialog for managing aircraft features."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Особенности самолетов")

        self.type_combo = PlaneTypeComboBox()
        self.type_combo.changed.connect(self.on_type_changed)

        self.setup_ui(OsobTable, {"parent": self})
        self.main_layout.insertWidget(0, self.type_combo)

    def on_type_changed(self, plane_type: Any) -> None:
        """Filter table by aircraft type."""
        if plane_type:
            self.table.table_model.load_data(plane_type)
        else:
            self.table.table_model.load_data(None)

    def add_item(self) -> None:
        from app.ui.dialogs.osob_features import OsobFeatureDialog

        dialog = OsobFeatureDialog(parent=self)
        dialog.updated.connect(self.refresh_data)
        if dialog.exec():
            self.updated.emit()

    def edit_item(self, item: Any) -> None:
        from app.ui.dialogs.osob_features import OsobFeatureDialog

        dialog = OsobFeatureDialog(osob=item, parent=self)
        dialog.updated.connect(self.refresh_data)
        if dialog.exec():
            self.updated.emit()

    def delete_item(self, item: Any) -> None:
        self.table.table_model.delete_item(item)
        self.refresh_data()
        self.updated.emit()

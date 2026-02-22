"""Dialogs for managing aircraft."""

from typing import Any

from PyQt6.QtWidgets import QLineEdit

from app.ui.dialogs.settings.base import UnAddEditDialog, UnDialog
from app.ui.widgets.combo_box import PlaneTypeComboBox, PodrazdComboBox
from app.ui.widgets.tables import PlanesTable
from app.ui.widgets.groups import OsobGroup
from data.models.aircraft import PlaneBase


class SettingsPlanes(UnDialog):
    """Dialog for managing aircraft."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Самолеты")
        self.setup_ui(PlanesTable)

        self.plane_type = PlaneTypeComboBox()
        self.plane_type.changed.connect(self.set_filter)
        self.podrazd = PodrazdComboBox()
        self.podrazd.changed.connect(self.set_filter)

        self.main_layout.insertWidget(0, self.plane_type)
        self.main_layout.insertWidget(1, self.podrazd)

    def set_filter(self) -> None:
        filter_dict = {
            "plane_type": self.plane_type.currentData(),
            "podrazd": self.podrazd.currentData(),
        }
        self.table.table_model.set_filter(filter_dict)

    def add_item(self) -> None:
        self.handle_dialog(AddPlane, "add")

    def edit_item(self, item: Any) -> None:
        self.handle_dialog(AddPlane, "edit", item)

    def delete_item(self, item: Any) -> None:
        self.table.table_model.delete_item(item)
        self.refresh_data()
        self.updated.emit()


class AddPlane(UnAddEditDialog):
    """Dialog for adding/editing aircraft."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Добавить самолет")

        self.type_combo = PlaneTypeComboBox()
        self.type_combo.changed.connect(self.set_osob_group)
        self.podrazd_combo = PodrazdComboBox()
        self.bort_edit = QLineEdit()
        self.zav_edit = QLineEdit()
        self.osob_group = OsobGroup()
        self.main_layout.addWidget(self.osob_group)
        self.form_layout.addRow("Тип самолета", self.type_combo)
        self.form_layout.addRow("Подразделение:", self.podrazd_combo)
        self.form_layout.addRow("Бортовой номер:", self.bort_edit)
        self.form_layout.addRow("Заводской номер:", self.zav_edit)
        self.form_layout.addRow("Модернизации:", self.osob_group)

    def set_osob_group(self, type):
        self.form_layout.removeRow(self.osob_group)
        self.osob_group = OsobGroup(type)
        self.form_layout.addRow("Модернизации:", self.osob_group)

    def edit_dialog(self, item: Any) -> None:
        super().edit_dialog(item)
        self.type_combo.setCurrentText(item.plane_type.name)
        self.podrazd_combo.setCurrentText(item.podrazd.name)
        self.bort_edit.setText(item.bort_number)
        self.zav_edit.setText(item.zav_num)

    def add_or_save_item(self) -> None:
        bort = self.bort_edit.text().strip()
        zav = self.zav_edit.text().strip()
        plane_type = self.type_combo.currentData()
        podrazd = self.podrazd_combo.currentData()

        if not bort:
            self.show_error("Бортовой номер не может быть пустым")
            return

        if not zav:
            self.show_error("Заводской номер не может быть пустым")
            return

        if plane_type is None:
            self.show_error("Выберите тип самолета")
            return

        if podrazd is None:
            self.show_error("Выберите подразделение")
            return

        if self.item:
            self.item.plane_type = plane_type
            self.item.podrazd = podrazd
            self.item.bort_number = bort
            self.item.zav_num = zav
            self.item.save()
        else:
            PlaneBase.create(
                plane_type=plane_type,
                podrazd=podrazd,
                bort_number=bort,
                zav_num=zav,
            )

        self.updated.emit()
        self.accept()

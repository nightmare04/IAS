"""Dialog for editing aircraft features with systems/blocks selection."""
from typing import Any

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QLineEdit,
    QMessageBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from app.ui.widgets.combo_box import PlaneTypeComboBox
from data.models.aircraft import AgregateBase, GroupBase, SystemBase
from data.models.osob import (
    OsobAgregateAddBase,
    OsobAgregateRemoveBase,
    OsobBase,
    OsobSystemAddBase,
    OsobSystemRemoveBase,
)


class OsobFeatureDialog(QDialog):
    """Dialog for editing aircraft feature with systems and blocks selection."""

    updated = pyqtSignal()

    def __init__(self, osob: OsobBase | None = None, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.osob = osob
        self.setWindowTitle("Редактирование особенности" if osob else "Добавление особенности")
        self.setModal(True)
        self.setMinimumSize(800, 600)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Basic info section
        self.basic_group = QGroupBox("Основная информация")
        self.basic_layout = QFormLayout()
        self.basic_group.setLayout(self.basic_layout)

        self.type_combo = PlaneTypeComboBox()
        self.name_edit = QLineEdit()

        self.basic_layout.addRow("Тип самолета", self.type_combo)
        self.basic_layout.addRow("Название особенности", self.name_edit)

        self.main_layout.addWidget(self.basic_group)

        # Tabs for systems and blocks
        self.tabs = QTabWidget()

        # Systems tab
        self.systems_widget = QWidget()
        self.systems_layout = QVBoxLayout()
        self.systems_widget.setLayout(self.systems_layout)

        self.systems_remove_group = QGroupBox("Удалить системы")
        self.systems_remove_layout = QVBoxLayout()
        self.systems_remove_group.setLayout(self.systems_remove_layout)

        self.systems_add_group = QGroupBox("Добавить системы")
        self.systems_add_layout = QVBoxLayout()
        self.systems_add_group.setLayout(self.systems_add_layout)

        self.systems_layout.addWidget(self.systems_remove_group)
        self.systems_layout.addWidget(self.systems_add_group)
        self.systems_layout.addStretch()

        self.tabs.addTab(self.systems_widget, "Системы")

        # Blocks tab
        self.blocks_widget = QWidget()
        self.blocks_layout = QVBoxLayout()
        self.blocks_widget.setLayout(self.blocks_layout)

        self.blocks_remove_group = QGroupBox("Удалить блоки/агрегаты")
        self.blocks_remove_layout = QVBoxLayout()
        self.blocks_remove_group.setLayout(self.blocks_remove_layout)

        self.blocks_add_group = QGroupBox("Добавить блоки/агрегаты")
        self.blocks_add_layout = QVBoxLayout()
        self.blocks_add_group.setLayout(self.blocks_add_layout)

        self.blocks_layout.addWidget(self.blocks_remove_group)
        self.blocks_layout.addWidget(self.blocks_add_group)
        self.blocks_layout.addStretch()

        self.tabs.addTab(self.blocks_widget, "Блоки/Агрегаты")

        self.main_layout.addWidget(self.tabs)

        # Buttons
        self.button_box = QDialogButtonBox()
        self.save_button = self.button_box.addButton("Сохранить", QDialogButtonBox.ButtonRole.AcceptRole)
        self.cancel_button = self.button_box.addButton("Отмена", QDialogButtonBox.ButtonRole.RejectRole)
        self.save_button.clicked.connect(self.save_item)  # type: ignore
        self.cancel_button.clicked.connect(self.reject)  # type: ignore

        self.main_layout.addWidget(self.button_box)

        # Store checkboxes
        self.system_remove_checks: dict[int, QCheckBox] = {}
        self.system_add_checks: dict[int, QCheckBox] = {}
        self.block_remove_checks: dict[int, QCheckBox] = {}
        self.block_add_checks: dict[int, QCheckBox] = {}
        self.system_to_blocks_map: dict[int, list[int]] = {}  # system_id -> [block_ids]

        # Connect type change to update lists
        self.type_combo.changed.connect(self.on_type_changed)

        if osob:
            self.load_data()
        else:
            # Enable save only when type is selected
            self.save_button.setEnabled(False) # type: ignore

    def on_type_changed(self, plane_type: Any) -> None:
        """Update systems and blocks lists when type changes."""
        if plane_type:
            self.save_button.setEnabled(True) # type: ignore
            self.load_systems()
            self.load_blocks()
        else:
            self.save_button.setEnabled(False) # type: ignore
            self.clear_lists()

    def load_data(self) -> None:
        """Load existing feature data."""
        self.name_edit.setText(self.osob.name)  # type: ignore
        self.type_combo.setCurrentText(self.osob.plane_type.name)  # type: ignore
        self.load_systems()
        self.load_blocks()

    def load_systems(self) -> None:
        """Load systems for selected aircraft type."""
        # Clear existing checkboxes
        self._clear_checkboxes(self.system_remove_checks)
        self._clear_checkboxes(self.system_add_checks)

        plane_type = self.type_combo.currentData()
        if not plane_type:
            return

        # Get all systems for this type
        all_systems = list(SystemBase.select().join(GroupBase).where(GroupBase.plane_type == plane_type))

        # Get systems to remove/add for this feature
        systems_to_remove = set()
        systems_to_add = set()

        if self.osob:
            systems_to_remove = {
                s.system.id for s in OsobSystemRemoveBase.select().where(OsobSystemRemoveBase.osob == self.osob)
            }
            systems_to_add = {
                s.system.id for s in OsobSystemAddBase.select().where(OsobSystemAddBase.osob == self.osob)
            }

        # Create checkboxes for remove AND add (same systems for both)
        for system in all_systems:
            # For remove
            cb_remove = QCheckBox(f"{system.name} (Группа: {system.group.name})")
            cb_remove.setChecked(system.id in systems_to_remove)
            self.systems_remove_layout.addWidget(cb_remove)
            self.system_remove_checks[system.id] = cb_remove
            cb_remove.stateChanged.connect(lambda state, sys_id=system.id: self.on_system_toggled(sys_id, "remove"))

            # For add
            cb_add = QCheckBox(f"{system.name} (Группа: {system.group.name})")
            cb_add.setChecked(system.id in systems_to_add)
            self.systems_add_layout.addWidget(cb_add)
            self.system_add_checks[system.id] = cb_add
            cb_add.stateChanged.connect(lambda state, sys_id=system.id: self.on_system_toggled(sys_id, "add"))

    def load_blocks(self) -> None:
        """Load blocks for selected aircraft type."""
        # Clear existing checkboxes
        self._clear_checkboxes(self.block_remove_checks)
        self._clear_checkboxes(self.block_add_checks)
        self.system_to_blocks_map.clear()

        plane_type = self.type_combo.currentData()
        if not plane_type:
            return

        # Get all blocks for this type
        all_blocks = list(
            AgregateBase.select()
            .join(SystemBase)
            .join(GroupBase)
            .where(GroupBase.plane_type == plane_type)
        )

        # Get blocks to remove/add for this feature
        blocks_to_remove = set()
        blocks_to_add = set()

        if self.osob:
            blocks_to_remove = {
                b.agregate.id for b in OsobAgregateRemoveBase.select().where(OsobAgregateRemoveBase.osob == self.osob)
            }
            blocks_to_add = {
                b.agregate.id for b in OsobAgregateAddBase.select().where(OsobAgregateAddBase.osob == self.osob)
            }

        # Create checkboxes for remove AND add (same blocks for both)
        for block in all_blocks:
            # For remove
            cb_remove = QCheckBox(f"{block.name} (Система: {block.system.name})")
            cb_remove.setChecked(block.id in blocks_to_remove)
            self.blocks_remove_layout.addWidget(cb_remove)
            self.block_remove_checks[block.id] = cb_remove
            cb_remove.stateChanged.connect(lambda state, blk_id=block.id: self.on_block_toggled(blk_id, "remove"))
            
            # Add to system->blocks mapping for remove
            sys_id = block.system.id
            if sys_id not in self.system_to_blocks_map:
                self.system_to_blocks_map[sys_id] = []
            self.system_to_blocks_map[sys_id].append(block.id)

            # For add
            cb_add = QCheckBox(f"{block.name} (Система: {block.system.name})")
            cb_add.setChecked(block.id in blocks_to_add)
            self.blocks_add_layout.addWidget(cb_add)
            self.block_add_checks[block.id] = cb_add
            cb_add.stateChanged.connect(lambda state, blk_id=block.id: self.on_block_toggled(blk_id, "add"))
            
            # Add to system->blocks mapping for add (same blocks)
            if sys_id not in self.system_to_blocks_map:
                self.system_to_blocks_map[sys_id] = []
            if block.id not in self.system_to_blocks_map[sys_id]:
                self.system_to_blocks_map[sys_id].append(block.id)

    def _clear_checkboxes(self, checks_dict: dict) -> None:
        """Clear and delete checkboxes."""
        for cb in checks_dict.values():
            cb.deleteLater()
        checks_dict.clear()

    def on_system_toggled(self, system_id: int, action: str) -> None:
        """Handle system checkbox toggle - auto-select corresponding blocks."""
        if action == "remove":
            system_cb = self.system_remove_checks.get(system_id)
            blocks_checks = self.block_remove_checks
        else:
            system_cb = self.system_add_checks.get(system_id)
            blocks_checks = self.block_add_checks

        if not system_cb:
            return

        is_checked = system_cb.isChecked()

        # Get all blocks for this system from our mapping
        system_blocks = self.system_to_blocks_map.get(system_id, [])

        # Toggle all blocks for this system that are in our checkboxes
        for block_id in system_blocks:
            if block_id in blocks_checks:
                blocks_checks[block_id].setChecked(is_checked)

    def on_block_toggled(self, block_id: int, action: str) -> None:
        """Handle block checkbox toggle - auto-select corresponding system if all blocks are selected."""
        if action == "remove":
            block_cb = self.block_remove_checks.get(block_id)
            blocks_checks = self.block_remove_checks
            system_checks = self.system_remove_checks
        else:
            block_cb = self.block_add_checks.get(block_id)
            blocks_checks = self.block_add_checks
            system_checks = self.system_add_checks

        if not block_cb:
            return

        # Get block system from DB
        block = AgregateBase.get_by_id(block_id)
        system_id = block.system.id

        # Get all blocks for this system from our mapping
        system_blocks_in_list = self.system_to_blocks_map.get(system_id, [])

        # Check if all visible blocks for this system are selected
        all_blocks_checked = all(
            blocks_checks[blk_id].isChecked()
            for blk_id in system_blocks_in_list
        )

        # Update system checkbox only if there are blocks in the list
        if system_id in system_checks and system_blocks_in_list:
            system_checks[system_id].setChecked(all_blocks_checked)

    def clear_lists(self) -> None:
        """Clear all checkbox lists."""
        self._clear_checkboxes(self.system_remove_checks)
        self._clear_checkboxes(self.system_add_checks)
        self._clear_checkboxes(self.block_remove_checks)
        self._clear_checkboxes(self.block_add_checks)

    def save_item(self) -> None:
        """Save feature with systems and blocks selections."""
        name = self.name_edit.text().strip()
        plane_type = self.type_combo.currentData()

        if not name:
            self.show_error("Название особенности не может быть пустым")
            return

        if plane_type is None:
            self.show_error("Выберите тип самолета")
            return

        try:
            # Create or update feature
            if self.osob:
                self.osob.name = name # type: ignore
                self.osob.plane_type = plane_type
                self.osob.save()

                # Delete existing relations
                OsobSystemRemoveBase.delete().where(OsobSystemRemoveBase.osob == self.osob).execute()
                OsobSystemAddBase.delete().where(OsobSystemAddBase.osob == self.osob).execute()
                OsobAgregateRemoveBase.delete().where(OsobAgregateRemoveBase.osob == self.osob).execute()
                OsobAgregateAddBase.delete().where(OsobAgregateAddBase.osob == self.osob).execute()
            else:
                self.osob = OsobBase.create(name=name, plane_type=plane_type)

            # Save systems to remove
            for system_id, cb in self.system_remove_checks.items():
                if cb.isChecked():
                    system = SystemBase.get_by_id(system_id)
                    OsobSystemRemoveBase.create(osob=self.osob, system=system)

            # Save systems to add
            for system_id, cb in self.system_add_checks.items():
                if cb.isChecked():
                    system = SystemBase.get_by_id(system_id)
                    OsobSystemAddBase.create(osob=self.osob, system=system)

            # Save blocks to remove
            for block_id, cb in self.block_remove_checks.items():
                if cb.isChecked():
                    block = AgregateBase.get_by_id(block_id)
                    OsobAgregateRemoveBase.create(osob=self.osob, agregate=block)

            # Save blocks to add
            for block_id, cb in self.block_add_checks.items():
                if cb.isChecked():
                    block = AgregateBase.get_by_id(block_id)
                    OsobAgregateAddBase.create(osob=self.osob, agregate=block)

            self.updated.emit()
            self.accept()

        except Exception as e:
            self.show_error(f"Ошибка при сохранении: {str(e)}")

    def show_error(self, message: str) -> None:
        """Show error message."""
        QMessageBox.warning(self, "Ошибка", message)

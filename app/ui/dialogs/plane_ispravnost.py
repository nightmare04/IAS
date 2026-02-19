"""Aircraft serviceability dialog."""
from typing import Any

from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.models.aircraft import GroupBase, PlaneBase
from app.models.failures import OtkazAgregateBase
from app.ui.widgets.tables import IspravnostTable, IspravnostTableModel


class IspravnostFrame(QFrame):
    """Frame displaying aircraft by division."""

    def __init__(self) -> None:
        super().__init__()
        self.podr_layout = QGridLayout()
        self.setLayout(self.podr_layout)
        self.load_data()

    def load_data(self) -> None:
        """Load divisions with aircraft."""
        from app.models.aircraft import PodrazdBase
        from app.ui.widgets.groups import PodrGroup

        podr_data = PodrazdBase.select()
        for i, podr in enumerate(podr_data):
            group = PodrGroup(podr)
            group.open_signal.connect(self.open_dialog)
            row = i // 2
            col = i % 2
            self.podr_layout.addWidget(group, row, col)

    def open_dialog(self, btn: Any) -> None:
        """Open aircraft serviceability dialog."""

        dialog = PlaneIspravnost(btn.plane)
        dialog.exec()
        btn.update_color()

    def clear_layout(self, layout: QGridLayout) -> None:
        """Clear all widgets from layout."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.deleteLater()
            else:
                sublayout = item.layout()
                if sublayout is not None:
                    self.clear_layout(sublayout)

    def update_podr(self) -> None:
        """Update divisions display."""
        self.clear_layout(self.podr_layout)
        self.load_data()


class PlaneIspravnost(QDialog):
    """Dialog for viewing and editing aircraft serviceability."""

    def __init__(self, plane: PlaneBase, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.plane = plane
        self.setWindowTitle(f"Исправность самолета {self.plane.plane_type.name} №{self.plane.bort_number}")
        self.setGeometry(100, 100, 800, 600)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.control_panel = QWidget()
        self.control_layout = QHBoxLayout(self.control_panel)

        self.filter_combo = QComboBox()
        self.filter_combo.addItem("Все группы")
        groups = GroupBase.select().order_by(GroupBase.name)
        for group in groups:
            self.filter_combo.addItem(group.name)
        self.filter_combo.currentTextChanged.connect(self.filter_by_category)

        self.add_btn = QPushButton("➕ Добавить блок / агрегат")
        self.add_btn.clicked.connect(self.add_item)

        self.control_layout.addWidget(QLabel("Фильтр по группе:"))
        self.control_layout.addWidget(self.filter_combo)
        self.control_layout.addStretch()

        self.osob_btn = QPushButton("⚙️ Особенности")
        self.osob_btn.clicked.connect(self.open_osob_dialog)
        self.control_layout.addWidget(self.osob_btn)

        self.add_btn = QPushButton("➕ Добавить блок / агрегат")
        self.add_btn.clicked.connect(self.add_item)

        self.control_layout.addWidget(self.add_btn)

        self.table_view = IspravnostTable(plane=plane)
        self.table_view.edit_signal.connect(self.edit_item)
        self.table_view.delete_signal.connect(self.delete_item)
        self.setup_ui()
        self.load_data()

    def filter_by_category(self, category: str) -> None:
        """Filter table by category."""
        self.load_data(category_filter=category)

    def open_osob_dialog(self) -> None:
        """Open dialog for selecting aircraft features."""
        from app.ui.dialogs.select_osob import SelectOsobDialog

        dialog = SelectOsobDialog(self.plane, self)
        dialog.exec()

    def edit_item(self, item: Any) -> None:
        """Edit failure item."""
        dialog = AddOtkazDialog(plane=self.plane, item=item)
        if dialog.exec():
            self.refresh_data()

    def add_item(self) -> None:
        """Add new failure item."""
        dialog = AddOtkazDialog(plane=self.plane)
        if dialog.exec():
            self.refresh_data()

    def delete_item(self, item: Any) -> None:
        """Delete failure item."""
        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            "Вы уверены, что хотите удалить этот элемент?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                item.delete_instance()
                self.refresh_data()
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось удалить элемент: {str(e)}")

    def refresh_data(self) -> None:
        """Refresh table data."""
        self.load_data()

    def on_double_click(self, index: Any) -> None:
        """Handle double click on table row."""
        model = self.table_view.model()
        if isinstance(model, IspravnostTableModel):
            item = model.get_item(index)
            if item:
                dialog = AddOtkazDialog(plane=self.plane, item=item)
                if dialog.exec():
                    self.refresh_data()

    def setup_ui(self) -> None:
        """Setup UI components."""
        self.main_layout.addWidget(self.control_panel)
        self.main_layout.addWidget(self.table_view)

        self.table_view.setSortingEnabled(False)
        self.table_view.doubleClicked.connect(self.on_double_click)

    def load_data(self, category_filter: str | None = None) -> None:
        """Load failure data."""
        self.table_view.table_model.load_data()
        self.table_view.set_span_for_groups()


class AddOtkazDialog(QDialog):
    """Dialog for adding/editing failure records."""

    def __init__(
        self, plane: PlaneBase, item: OtkazAgregateBase | None = None, parent: Any | None = None
    ) -> None:
        super().__init__(parent)
        self.plane = plane
        self.item = item
        self.setWindowTitle("Добавление отказавшего блока/агрегата")
        self.setModal(True)
        self.setFixedSize(350, 250)

        from app.ui.widgets.combo_box import AgregateComboBox, GroupComboBox, SystemComboBox

        self.group_combo = GroupComboBox()
        self.system_combo = SystemComboBox()
        self.agregate_combo = AgregateComboBox()

        self.group_combo.changed.connect(self.on_group_changed)
        self.system_combo.changed.connect(self.on_system_changed)

        self.agregate_number = QLineEdit()
        self.remove_checkbox = QCheckBox()
        self.desc = QLineEdit()

        self.button_box = QDialogButtonBox()
        self.save_button = self.button_box.addButton("Сохранить", QDialogButtonBox.ButtonRole.AcceptRole)
        self.cancel_button = self.button_box.addButton("Отмена", QDialogButtonBox.ButtonRole.RejectRole)
        self.save_button.clicked.connect(self.edit_create_item)  # type: ignore
        self.cancel_button.clicked.connect(self.reject)  # type: ignore

        form_layout = QFormLayout()
        form_layout.addRow("Группа обслуживания:", self.group_combo)
        form_layout.addRow("Система самолета:", self.system_combo)
        form_layout.addRow("Агрегат/блок:", self.agregate_combo)
        form_layout.addRow("Номер блока/агрегата:", self.agregate_number)
        form_layout.addRow("Агрегат снят?", self.remove_checkbox)
        form_layout.addRow("Примечание:", self.desc)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.button_box)

        self.setLayout(layout)
        if item:
            self.load_data()

    def on_group_changed(self, group: Any) -> None:
        """Update system combo filter when group changes."""
        if group:
            # Get available systems considering features
            from app.models.osob import get_available_systems_for_plane

            available_systems = get_available_systems_for_plane(self.plane, group)
            self.system_combo._model.set_custom_data(available_systems)
            self.system_combo._model.refresh()

    def on_system_changed(self, system: Any) -> None:
        """Update agregate combo filter when system changes."""
        if system:
            # Get available agregates considering features
            from app.models.osob import get_available_agregates_for_plane

            available_agregates = get_available_agregates_for_plane(self.plane, system)
            self.agregate_combo._model.set_custom_data(available_agregates)
            self.agregate_combo._model.refresh()

    def load_data(self) -> None:
        """Load existing item data."""
        self.setWindowTitle("Редактирование отказавшего блока/агрегата")

        # First set group to trigger cascade updates
        group = self.item.agregate.system.group  # type: ignore
        self.group_combo._model.filter = {"plane_type": self.plane.plane_type}
        self.group_combo._model.load_data()

        # Find group index and select it
        for i in range(self.group_combo.count()):
            if self.group_combo.itemData(i) == group:
                self.group_combo.setCurrentIndex(i)
                break

        # Now set system (will be filtered by on_group_changed)
        system = self.item.agregate.system  # type: ignore
        self.on_group_changed(group)

        # Find system index and select it
        for i in range(self.system_combo.count()):
            if self.system_combo.itemData(i) == system:
                self.system_combo.setCurrentIndex(i)
                break

        # Now set agregate (will be filtered by on_system_changed)
        agregate = self.item.agregate  # type: ignore
        self.on_system_changed(system)

        # Find agregate index and select it
        for i in range(self.agregate_combo.count()):
            if self.agregate_combo.itemData(i) == agregate:
                self.agregate_combo.setCurrentIndex(i)
                break

        self.agregate_number.setText(str(self.item.number))  # type: ignore
        self.remove_checkbox.setChecked(self.item.removed)  # type: ignore
        self.desc.setText(str(self.item.description))  # type: ignore

    def edit_create_item(self) -> None:
        """Save or update item."""
        if self.item:
            try:
                self.item.agregate = self.agregate_combo.currentData()
                self.item.plane = self.plane.id
                self.item.number = self.agregate_number.text()
                self.item.removed = self.remove_checkbox.isChecked()
                self.item.description = self.desc.text()
                self.item.save()
                self.accept()
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось изменить агрегат/блок: {str(e)}")
        else:
            try:
                agregate = self.agregate_combo.currentData()
                OtkazAgregateBase.create(
                    agregate=agregate,
                    plane=self.plane.id,
                    number=self.agregate_number.text(),
                    removed=self.remove_checkbox.isChecked(),
                    description=self.desc.text(),
                )
                self.accept()
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось добавить агрегат/блок: {str(e)}")

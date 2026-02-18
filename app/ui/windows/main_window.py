"""Main window for IAS application."""
from typing import Any

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QVBoxLayout, QWidget

from app.ui.dialogs.plane_ispravnost import IspravnostFrame
from app.ui.dialogs.settings import (
    SettingsAgregate,
    SettingsGroup,
    SettingsOsob,
    SettingsPlanes,
    SettingsPlaneType,
    SettingsPodrazd,
    SettingsSystem,
)
from app.ui.widgets.buttons import IASButton


class MainForm(QMainWindow):
    """Main application window."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.menu = self.menuBar()

        settings_menu = self.menu.addMenu("&Настройки")
        type_action = QAction("Типы самолетов", self)
        type_action.triggered.connect(self.plane_type_dialog)
        osob_action = QAction("Особенности самолетов", self)
        osob_action.triggered.connect(self.osob_dialog)
        podr_action = QAction("Подразделения", self)
        podr_action.triggered.connect(self.podr_dialog)
        group_action = QAction("Группы обслуживания", self)
        group_action.triggered.connect(self.group_dialog)
        system_action = QAction("Системы самолетов", self)
        system_action.triggered.connect(self.system_dialog)
        planes_action = QAction("Самолеты", self)
        planes_action.triggered.connect(self.planes_dialog)
        agreg_action = QAction("Блоки/агрегаты", self)
        agreg_action.triggered.connect(self.agregate_dialog)

        settings_menu.addAction(type_action)
        settings_menu.addAction(osob_action)
        settings_menu.addAction(podr_action)
        settings_menu.addAction(group_action)
        settings_menu.addAction(system_action)
        settings_menu.addSeparator()
        settings_menu.addAction(planes_action)
        settings_menu.addAction(agreg_action)

        self.setWindowTitle("Исправность")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.frame = IspravnostFrame()
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.frame, stretch=8)
        self.central_widget.setLayout(main_layout)

    def osob_dialog(self) -> None:
        """Open aircraft features dialog."""
        dialog = SettingsOsob(self)
        dialog.exec()

    def plane_type_dialog(self) -> None:
        """Open aircraft types dialog."""
        dialog = SettingsPlaneType(self)
        dialog.exec()

    def podr_dialog(self) -> None:
        """Open divisions dialog."""
        dialog = SettingsPodrazd(self)
        dialog.updated.connect(self.frame.update_podr)
        dialog.exec()

    def group_dialog(self) -> None:
        """Open maintenance groups dialog."""
        dialog = SettingsGroup(self)
        dialog.exec()

    def system_dialog(self) -> None:
        """Open aircraft systems dialog."""
        dialog = SettingsSystem(self)
        dialog.exec()

    def agregate_dialog(self) -> None:
        """Open aggregates dialog."""
        dialog = SettingsAgregate(self)
        dialog.exec()

    def planes_dialog(self) -> None:
        """Open aircraft dialog."""
        dialog = SettingsPlanes()
        dialog.updated.connect(self.frame.update_podr)
        dialog.exec()

    def create_button_panel(self) -> QWidget:
        """Create button panel (currently unused)."""
        panel = QWidget()
        layout = QVBoxLayout()

        self.condition_btn = IASButton("Исправность")
        self.condition_btn.setMinimumHeight(40)

        self.malfunction_btn = IASButton("Отказы")
        self.malfunction_btn.setMinimumHeight(40)

        self.search_btn = IASButton("Поиск блоков/агрегатов")
        self.search_btn.setMinimumHeight(40)

        layout.addWidget(self.condition_btn)
        layout.addWidget(self.malfunction_btn)
        layout.addWidget(self.search_btn)
        layout.addStretch()
        panel.setLayout(layout)
        return panel

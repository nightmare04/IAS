from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
)

from custom_components.buttons import IASButton
from forms.plane_ispravnost import IspravnostFrame
from forms.settings import SettingsPlaneType, SettingsPodrazd, SettingsGroup


class MainForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.menu = self.menuBar()

        settings_menu = self.menu.addMenu("&Настройки")
        type_action = QAction('Типы самолетов', self)
        type_action.triggered.connect(self.plane_type_dialog)
        podr_action = QAction('Подразделения', self)
        podr_action.triggered.connect(self.podr_dialog)
        group_action = QAction('Группы обслуживания', self)
        group_action.triggered.connect(self.group_dialog)
        agreg_action = QAction('Системы/агрегаты', self)

        settings_menu.addAction(type_action)
        settings_menu.addAction(podr_action)
        settings_menu.addAction(group_action)
        settings_menu.addSeparator()
        settings_menu.addAction(agreg_action)

        self.setWindowTitle("Исправность")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.frame = IspravnostFrame()
        main_layout = QHBoxLayout()
        button_panel = self.create_button_panel()
        main_layout.addWidget(button_panel, stretch=2)
        main_layout.addWidget(self.frame, stretch=8)
        self.central_widget.setLayout(main_layout)

    def plane_type_dialog(self):
        dialog = SettingsPlaneType()
        dialog.exec()

    def podr_dialog(self):
        dialog = SettingsPodrazd()
        dialog.exec()

    def group_dialog(self):
        dialog = SettingsGroup()
        dialog.exec()

    def create_button_panel(self) -> QWidget:
        """Создание панели кнопок"""
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
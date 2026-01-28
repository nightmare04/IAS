from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFrame,
)
from .custom_mod import IASButton


class MainForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.menu = self.menuBar()

        self.init_ui()

    def init_ui(self):
        settings_menu = self.menu.addMenu("&Настройки")
        type_action = QAction('Типы самолетов', self)
        podr_action = QAction('Подразделения', self)
        spec_action = QAction('Специальности', self)
        agreg_action = QAction('Системы/агрегаты', self)

        settings_menu.addAction(type_action)
        settings_menu.addAction(podr_action)
        settings_menu.addAction(spec_action)
        settings_menu.addSeparator()
        settings_menu.addAction(agreg_action)

        self.setWindowTitle("Исправность")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.frame = QFrame ()
        main_layout = QHBoxLayout()
        button_panel = self.create_button_panel()
        main_layout.addWidget(button_panel, stretch=2)
        main_layout.addWidget(self.frame, stretch=8)
        self.central_widget.setLayout(main_layout)


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
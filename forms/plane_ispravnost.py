from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QLabel, QMessageBox

from data import PlaneBase, GroupBase, AgregateBase, OtkazAgregateBase, PlaneSystemBase
from forms.custom_components.tables import IspravnostTableModel, IspravnostTableView
from forms.otkaz_dialog import AddOtkazDialog


class PlaneIspravnost(QDialog):
    def __init__(self, plane : PlaneBase, parent=None, ):
        super().__init__(parent)
        self.plane = plane
        self.setWindowTitle(f"Исправность самолета {self.plane.plane_type.name} №{self.plane.bort_number}")
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = QWidget(self)
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
        self.add_btn.clicked.connect(self.add_otkaz)

        self.control_layout.addWidget(QLabel("Фильтр по группе:"))
        self.control_layout.addWidget(self.filter_combo)
        self.control_layout.addStretch()
        self.control_layout.addWidget(self.add_btn)

        self.status_label = QLabel("Загрузка данных...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
             QLabel {
                 background-color: #f0f0f0;
                 padding: 5px;
                 border-top: 1px solid #cccccc;
                 font-weight: bold;
             }
         """)

        headers = ["Наименование", "Система", "Номер агрегата/блока", "Примечание"]
        self.model = IspravnostTableModel(headers=headers, data=OtkazAgregateBase.select().where(id == self.plane.id))
        self.table_view = IspravnostTableView()
        self.table_view.setModel(self.model)
        self.setup_ui()
        self.load_data()

    def filter_by_category(self, category):
        self.load_data(category_filter=category)

    def add_otkaz(self):
        dialog = AddOtkazDialog(self.plane)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_data()

    def refresh_data(self):
        self.load_data()

    def on_double_click(self):
        pass

    def setup_ui(self):
        self.main_layout.addWidget(self.control_panel)
        self.main_layout.addWidget(self.table_view)
        self.main_layout.addWidget(self.status_label)

        # Настройка таблицы
        self.table_view.setSpanForGroups()
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.setSortingEnabled(False)

        # Подключаем двойной клик
        self.table_view.doubleClicked.connect(self.on_double_click)


    def load_data(self, category_filter=None):
        try:
            query = (OtkazAgregateBase
                     .select()
                     .join(AgregateBase)
                     .join(PlaneSystemBase)
                     .join(GroupBase)
                     .where(OtkazAgregateBase.plane == self.plane.id))

            if category_filter and category_filter != "Все группы":
                query = query.where(GroupBase.name == category_filter)

            self.model.load_data(query)
            self.table_view.setSpanForGroups()

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при загрузке данных: {str(e)}")





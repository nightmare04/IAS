from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QLabel, QMessageBox

from data import PlaneBase, PlaneTypeBase, GroupBase, AgregateBase, OtkazAgregateBase
from forms.custom_components.tables import IspravnostTableModel, IspravnostTableView


class PlaneIspravnost(QDialog):
    def __init__(self, plane : PlaneBase, parent=None, ):
        super().__init__(parent)
        self.plane = plane
        self.parent = parent
        self.setWindowTitle(f"Исправность самолета {PlaneTypeBase.get_by_id(self.plane.plane_type)} {self.plane.bort_number}")
        self.setGeometry(100, 100, 800, 600)

        self.create_widgets()
        self.setup_ui()
        
    def create_widgets(self):
        self.central_widget = QWidget(self)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.control_panel = QWidget()
        self.control_layout = QHBoxLayout(self.control_panel)
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("Все группы")
        groups = GroupBase.select().order_by(GroupBase.name)
        for group in groups:
            self.filter_combo.addItem(group.name)

        self.filter_combo.currentTextChanged.connect(self.filter_by_category)

        self.add_btn = QPushButton("➕ Добавить продукт")
        self.add_btn.clicked.connect(self.add_product)

        self.refresh_btn = QPushButton("🔄 Обновить")
        self.refresh_btn.clicked.connect(self.refresh_data)

        self.control_layout.addWidget(QLabel("Фильтр по категории:"))
        self.control_layout.addWidget(self.filter_combo)
        self.control_layout.addStretch()
        self.control_layout.addWidget(self.add_btn)
        self.control_layout.addWidget(self.refresh_btn)

        headers = ["Наименование", "Система", "Номер агрегата/блока", "Примечание"]
        self.model = IspravnostTableModel(headers=headers, plane=self.plane)
        self.table_view = IspravnostTableView()

    def filter_by_category(self):
        pass

    def add_product(self):
        pass

    def refresh_data(self):
        pass

    def on_double_click(self):
        pass

    def setup_ui(self):
        self.main_layout.addWidget(self.control_panel)
        self.main_layout.addWidget(self.table_view)

        # Настройка таблицы
        self.table_view.setSpanForGroups()
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.setSortingEnabled(True)

        # Подключаем двойной клик
        self.table_view.doubleClicked.connect(self.on_double_click)

    def load_data(self, category_filter=None):
        try:
            query = (OtkazAgregateBase
                     .select(AgregateBase, PlaneBase, GroupBase)
                     .join(AgregateBase)
                     .where(PlaneBase.id == self.plane.id))

            if category_filter and category_filter != "Все группы":
                query = query.where(GroupBase.name == category_filter)

            self.model.load_data(query)
            self.table_view.setSpanForGroups()
            self.update_status_label(category_filter)

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при загрузке данных: {str(e)}")





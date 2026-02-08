from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QWidget, QHBoxLayout, QComboBox, QPushButton, QLabel, QMessageBox, \
    QFrame, QGridLayout

from custom_components.buttons import PlaneBtn
from custom_components.groups import PodrGroup
from custom_components.tables import IspravnostTableModel, IspravnostTableView
from data.data_models import PlaneBase, GroupBase, OtkazAgregateBase, AgregateBase, PlaneSystemBase, PodrazdBase
from forms.otkaz_dialog import AddOtkazDialog, EditOtkazDialog

class IspravnostFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.load_data()

    def load_data(self):
        podr_data = PodrazdBase.select()
        podr_layout = QGridLayout()
        for i, podr in enumerate(podr_data):
            group = PodrGroup(podr)
            group.load_planes()
            row = i // 2
            col = i % 2
            podr_layout.addWidget(group, row, col)
        self.setLayout(podr_layout)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.deleteLater()
            else:
                sublayout = item.layout()
                if sublayout is not None:
                    self.clear_layout(sublayout)

    def update_ispravnost(self):
        for plane_bnt in self.findChildren(PlaneBtn):
            plane_bnt.update_color()


class PlaneIspravnost(QDialog):
    def __init__(self, plane : PlaneBase, parent=None, ):
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
        self.add_btn.clicked.connect(self.add_otkaz)

        self.control_layout.addWidget(QLabel("Фильтр по группе:"))
        self.control_layout.addWidget(self.filter_combo)
        self.control_layout.addStretch()
        self.control_layout.addWidget(self.add_btn)

        self.status_label = QLabel("Загрузка данных...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.status_label.setStyleSheet("""
             QLabel {
                 background-color: #f0f0f0;
                 padding: 5px;
                 border-top: 1px solid #cccccc;
                 font-weight: bold;
             }
         """)

        self.model = IspravnostTableModel(data=OtkazAgregateBase.select().where(id == self.plane.id))
        self.table_view = IspravnostTableView(parent=self)
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

    def update_status(self, query):
        self.status_label.setText(f'Загружено {len(query)} блоков и агрегатов.')

    def on_double_click(self, index):
        model = self.table_view.model()
        if isinstance(model, IspravnostTableModel):
            row = index.row()
            item_id = model.get_item_id(row)
            if item_id:
                dialog = EditOtkazDialog(OtkazAgregateBase.get(item_id))
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    self.refresh_data()

    def setup_ui(self):
        self.main_layout.addWidget(self.control_panel)
        self.main_layout.addWidget(self.table_view)
        self.main_layout.addWidget(self.status_label)

        # Настройка таблицы
        self.table_view.set_span_for_groups()
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
            self.table_view.set_span_for_groups()
            self.update_status(query)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при загрузке данных: {str(e)}")





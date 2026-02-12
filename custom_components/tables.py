from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QTableView, QAbstractItemView, QSizePolicy, QHeaderView, QMessageBox, QMenu

from custom_components.tables_models import IspravnostTableModel, UnTableModel, PlanesTypesModel, PodrazdModel, \
    GroupModel, AgregateModel, PlanesModel
from data.data import OtkazAgregateBase
from forms.otkaz_dialog import EditOtkazDialog


class UnTableView(QTableView):
    edit_signal = pyqtSignal(int)
    delete_signal = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.table_model = UnTableModel()
        self.setAlternatingRowColors(False)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, position):
        index = self.indexAt(position)
        model = self.model()

        menu = QMenu(self)

        if index.isValid() and isinstance(model, UnTableModel):
            row = index.row()
            item_id = model.get_item_id(row)
            edit_action = QAction("✏️ Изменить элемент", self)
            edit_action.triggered.connect(lambda: self.edit_item(item_id))
            menu.addAction(edit_action)

            delete_action = QAction("🗑️ Удалить элемент", self)
            delete_action.triggered.connect(lambda: self.delete_item(item_id))
            menu.addAction(delete_action)

        menu.exec(self.viewport().mapToGlobal(position))

    def edit_item(self, item_id):
        self.edit_signal.emit(item_id)

    def delete_item(self, item_id):
        self.delete_signal.emit(item_id)


class IspravnostTableView(UnTableView):
    def __init__(self, parent=None):
        super().__init__(parent)

    def show_context_menu(self, position):
        index = self.indexAt(position)
        model = self.model()

        menu = QMenu(self)

        if index.isValid() and isinstance(model, IspravnostTableModel):
            row = index.row()
            row_type = model.get_row_type(row)
            item_id = model.get_item_id(row)

            if row_type == 'agregate' and item_id:
                edit_action = QAction("✏️ Изменить", self)
                edit_action.triggered.connect(lambda: self.edit_item(item_id))
                menu.addAction(edit_action)

                delete_action = QAction("🗑️ Удалить", self)
                delete_action.triggered.connect(lambda: self.delete_item(item_id))
                menu.addAction(delete_action)

        menu.exec(self.viewport().mapToGlobal(position))

    def set_span_for_groups(self):
        self.clear_all_span()
        model = self.model()
        if isinstance(model, IspravnostTableModel):
            for row in range(model.rowCount()):
                if model.is_group_row(row):
                    self.setSpan(row, 0, 1, model.columnCount())

    def clear_all_span(self):
        model = self.model()
        if isinstance(model, IspravnostTableModel):
            rows = model.rowCount()
            cols = model.columnCount()
            for row in range(rows):
                for col in range(cols):
                    if self.rowSpan(row, col) > 1:
                        self.setSpan(row, col, 1, 1)

    def edit_item(self, item_id):
        try:
            item = OtkazAgregateBase.get_by_id(item_id)
            dialog = EditOtkazDialog(item)
            dialog.exec()

        except OtkazAgregateBase.DoesNotExist:
            QMessageBox.warning(self, "Ошибка", "Блок/агрегат не найден!")

    def delete_item(self, item_id):
        self.model().delete_item(item_id)
        self.parent.refresh_data()


class PlaneTypesTable(UnTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.table_model = PlanesTypesModel()
        self.setModel(self.table_model)


class PodrazdTable(UnTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.table_model = PodrazdModel()
        self.setModel(self.table_model)


class GroupTable(UnTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.table_model = GroupModel()
        self.setModel(self.table_model)


class AgregateTable(UnTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.table_model = AgregateModel()
        self.setModel(self.table_model)


class PlanesTable(UnTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.table_model = PlanesModel()
        self.setModel(self.table_model)

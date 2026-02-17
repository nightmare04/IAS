from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QTableView, QAbstractItemView, QSizePolicy, QMenu, QHeaderView

from custom_components.tables_models import IspravnostTableModel, UnTableModel, PlanesTypesModel, PodrazdModel, \
    GroupModel, AgregateModel, PlanesModel, OsobModel
from data.data import PlaneBase



class UnTableView(QTableView):
    edit_signal = pyqtSignal(object)
    delete_signal = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.table_model = UnTableModel()
        self.setAlternatingRowColors(False)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents) # type: ignore
        header.setStretchLastSection(True) # type: ignore

    def show_context_menu(self, position):
        index = self.indexAt(position)
        model = self.model()

        menu = QMenu(self)

        if index.isValid():
            item = model.data(index, role=Qt.ItemDataRole.UserRole)
            edit_action = QAction("✏️ Изменить элемент", self)
            edit_action.triggered.connect(lambda: self.edit_item(item))
            menu.addAction(edit_action)
            delete_action = QAction("🗑️ Удалить элемент", self)
            delete_action.triggered.connect(lambda: self.delete_item(item))
            menu.addAction(delete_action)

        menu.exec(self.viewport().mapToGlobal(position)) # type: ignore

    def edit_item(self, item):
        self.edit_signal.emit(item)

    def delete_item(self, item):
        self.delete_signal.emit(item)


class IspravnostTable(UnTableView):
    def __init__(self, plane: PlaneBase, parent=None):
        super().__init__(parent)
        self.table_model = IspravnostTableModel(plane)
        self.setModel(self.table_model)

    def set_span_for_groups(self):
        self.clear_all_span()
        if isinstance(self.table_model, IspravnostTableModel):
            for row in range(self.table_model.rowCount()):
                if self.table_model.is_group_row(row):
                    self.setSpan(row, 0, 1, self.table_model.columnCount())

    def clear_all_span(self):
        if isinstance(self.table_model, IspravnostTableModel):
            rows = self.table_model.rowCount()
            cols = self.table_model.columnCount()
            for row in range(rows):
                for col in range(cols):
                    if self.rowSpan(row, col) > 1:
                        self.setSpan(row, col, 1, 1)

    def set_filter(self, filter):
        pass

    def load_data(self):
        self.table_model.load_data()
        self.clear_all_span()
        self.set_span_for_groups()




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

    def set_filter(self, filter_str):
        self.table_model.load_data(filter_str)


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
        
    def set_filter(self, filter_str):
        self.table_model.load_data(filter_str)


class OsobTable(UnTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.table_model = OsobModel()
        self.setModel(self.table_model)

from PyQt6.QtCore import QAbstractListModel, Qt, pyqtSignal
from PyQt6.QtWidgets import QComboBox
from data.data import TypeBase, GroupBase, SystemBase, AgregateBase, PodrazdBase


class ComboBoxModel(QAbstractListModel):
    
    def __init__(self, peewee_model=None, first_string=None, display_field='name', parent=None):
        super().__init__(parent)
        self._peewee_model = peewee_model
        self._first_string = first_string
        self.display_field = display_field
        self.filter = {}
        self._data = []
        self.load_data()

    def get_filtered_query(self):
        query = self._peewee_model.select() # type: ignore
        for k,v in self.filter.items():
            query = query.where(getattr(self._peewee_model, k) == v)
        return query

    def load_data(self):
        self._data = []
        query = self.get_filtered_query()
        self._data = list(query)
        if self._first_string:
            self._data.insert(0, self._first_string)

    def rowCount(self, parent=None):
        return len(self._data)

    def data(self, index, role=Qt.ItemDataRole):
        if not index.isValid() or index.row() >= len(self._data):
            return None

        item = self._data[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:
            if isinstance(item, str):
                return item
            return getattr(item, self.display_field)
        elif role == Qt.ItemDataRole.UserRole:
            return item

        return None

    def refresh(self):
        self.beginResetModel()
        self.load_data()
        self.endResetModel()


class IASComboBox(QComboBox):
    changed = pyqtSignal(object)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.currentIndexChanged.connect(self.emit_changed)
        
    def emit_changed(self, index):
        item = self.itemData(index, role=Qt.ItemDataRole.UserRole)
        self.changed.emit(item)
    
    def set_filter(self):
        pass    
        

class PlaneTypeComboBox(IASComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._model = ComboBoxModel(peewee_model=TypeBase, first_string='Выберите тип самолета')
        self.setModel(self._model)
        

class PodrazdComboBox(IASComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._model = ComboBoxModel(peewee_model=PodrazdBase, first_string='Выберите подразделение')
        self.setModel(self._model)


class GroupComboBox(IASComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._model = ComboBoxModel(peewee_model=GroupBase, first_string='Выберите группу обслуживания')
        self.setModel(self._model)

    def set_filter(self, plane_type: TypeBase):
        self._model.filter = {'plane_type': plane_type}
        self._model.load_data()
        
        
class SystemComboBox(IASComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._model = ComboBoxModel(peewee_model=SystemBase, first_string='Выберите систему самолета')
        self.setModel(self._model)

    def set_filter(self, group: GroupBase):
        self._model.filter = {'group': group}
        self._model.load_data()
        

class AgregateComboBox(IASComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._model = ComboBoxModel(peewee_model=AgregateBase, first_string='Выберите блок/агрегат самолета')
        self.setModel(self._model)

    def set_filter(self, system: SystemBase):
        self._model.filter = {'system': system}
        self._model.load_data()
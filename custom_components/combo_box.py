from PyQt6.QtCore import QAbstractListModel, Qt
from PyQt6.QtWidgets import QComboBox

from data.data import TypeBase, GroupBase, SystemBase, AgregateBase, PodrazdBase


class ComboBoxModel(QAbstractListModel):
    def __init__(self, peewee_model=None, first_string=None, display_field='name', parent=None):
        super().__init__(parent)
        self._peewee_model = peewee_model
        self._first_string = first_string
        self.display_field = display_field
        self.query_filter = None
        self._data = []
        self.load_data()

    def load_data(self):
        self._data = []
        if self.query_filter is not None:
            query = self.query_filter
        else:
            query = self._peewee_model.select()
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


class PlaneTypeComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._model = ComboBoxModel(peewee_model=TypeBase, first_string='Выберите тип самолета')
        self.setModel(self._model)


class PodrazdComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._model = ComboBoxModel(peewee_model=PodrazdBase, first_string='Выберите подразделение')
        self.setModel(self._model)


class GroupComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._model = ComboBoxModel(peewee_model=GroupBase, first_string='Выберите группу обслуживания')
        self.setModel(self._model)

    def set_filter(self, plane_type_str):
        plane_type = TypeBase.get_or_none(TypeBase.name == plane_type_str)
        query = (GroupBase
                 .select()
                 .where(GroupBase.plane_type == plane_type)
                 )
        self._model.query_filter = query
        self._model.refresh()


class SystemComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._model = ComboBoxModel(peewee_model=SystemBase, first_string='Выберите систему самолета')
        self.setModel(self._model)

    def set_filter(self, group_str):
        group = GroupBase.get_or_none(GroupBase.name == group_str)
        query = (SystemBase
                 .select()
                 .where(SystemBase.group == group)
                 )
        self._model.query_filter = query
        self._model.refresh()


class AgregateComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._model = ComboBoxModel(peewee_model=AgregateBase, first_string='Выберите блок/агрегат самолета')
        self.setModel(self._model)

    def set_filter(self, system_str):
        system = SystemBase.get_or_none(SystemBase.name == system_str)
        query = (AgregateBase
                 .select()
                 .where(AgregateBase.system == system)
                 )
        self._model.query_filter = query
        self._model.refresh()

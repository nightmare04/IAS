from PyQt6.QtCore import QAbstractListModel, Qt
from PyQt6.QtWidgets import QComboBox

from data.data import PlaneTypeBase, GroupBase, PlaneSystemBase, AgregateBase

class ComboBoxModel(QAbstractListModel):
    def __init__(self, peewee_model=None, display_field='name', query_filter=None, parent=None):
        super().__init__(parent)
        self.peewee_model = peewee_model
        self.display_field = display_field
        self.query_filter = query_filter
        self._data = []
        self.load_data()

    def load_data(self):
        query = self.peewee_model.select()
        if self.query_filter:
            query = query.where(self.query_filter)

        self._data = list(query)

    def rowCount(self, parent=None):
        return len(self._data)

    def data(self, index, role=Qt.ItemDataRole):
        if not index.isValid() or index.row() >= len(self._data):
            return None

        item = self._data[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:
            # Получаем значение поля для отображения
            return getattr(item, self.display_field)
        elif role == Qt.ItemDataRole.UserRole:
            # Возвращаем весь объект Peewee
            return item

        return None

    def refresh(self):
        """Обновление данных из базы"""
        self.beginResetModel()
        self.load_data()
        self.endResetModel()



class PlaneTypeComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_data()

    def load_data(self):
        self.clear()
        self.addItem("Выберите тип самолета", 0)
        list_data = PlaneTypeBase.select()
        for plane_type in list_data:
            self.addItem(plane_type.name, plane_type.id)


class GroupComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addItem("Сначала выберете тип самолета...")

    def load_data(self, data=None):
        self.clear()
        self.addItem("Выберите группу обслуживания", 0)
        if data is None:
            list_data = GroupBase.select()
        else:
            list_data = GroupBase.select().where(GroupBase.plane_type == data)

        for spec in list_data:
            self.addItem(spec.name, spec.id)


class SystemComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addItem("Сначала выберете группу обслуживания...")

    def load_data(self, data=None):
        self.clear()
        self.addItem("Выберите систему самолета")
        if data:
            list_data = PlaneSystemBase.select().where(PlaneSystemBase.group == data)
            for system in list_data:
                self.addItem(system.name, system.id)


class AgregateComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)

    def load_data(self, data=None):
        self.clear()
        self.addItem("Выберите блок/агрегат")
        if data:
            list_data = AgregateBase.select().where(AgregateBase.system == data)
            for agregate in list_data:
                self.addItem(agregate.name, agregate.id)

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt6.QtGui import QFont, QBrush, QColor

from data.data_models import PlaneTypeBase, PodrazdBase, GroupBase, OtkazAgregateBase


class IspravnostTableModel(QAbstractTableModel):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self._data = data
        self._headers = ["Наименование", "Система", "Номер агрегата/блока", "Примечание"]
        self._prepared_data = []
        self._group_rows = []
        self._group_values = []
        self._items_ids = []
        self._row_type = []

    def load_data(self, data):
        """Загружает данные из запроса Peewee"""
        self.beginResetModel()
        self._prepared_data = []
        self._group_rows = []
        self._group_values = []
        self._items_ids = []
        self._row_type = []

        # Сортируем по категории
        sorted_data = sorted(data, key=lambda x: str(x.agregate.system.name))

        current_group = None
        row_idx = 0

        for item in sorted_data:
            group_value = str(item.agregate.system.group.name)

            # Если началась новая группа
            if group_value != current_group:
                # Добавляем строку группы
                self._prepared_data.append([group_value] * (len(self._headers)))
                self._group_rows.append(row_idx)
                self._items_ids.append(None)
                self._row_type.append('group')
                row_idx += 1
                current_group = group_value

            # Добавляем обычную строку данных
            row_data = [item.agregate.name, item.agregate.system.name, item.number, item.description]
            self._prepared_data.append(row_data)
            self._items_ids.append(item.id)
            self._row_type.append('agregate')
            row_idx += 1

        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return len(self._prepared_data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()

        if 0 <= row < len(self._prepared_data) and 0 <= col < len(self._headers):
            if role == Qt.ItemDataRole.DisplayRole:
                value = self._prepared_data[row][col]
                return str(value) if value is not None else ""

            elif role == Qt.ItemDataRole.FontRole and row in self._group_rows:
                font = QFont()
                font.setBold(True)
                font.setPointSize(10)
                return font

            elif role == Qt.ItemDataRole.BackgroundRole:
                if self._row_type[row] == 'group':
                    return QBrush(QColor(220, 220, 220))
                return QBrush(QColor(255, 255, 255))

            elif role == Qt.ItemDataRole.TextAlignmentRole and row in self._group_rows:
                if col == 0:
                    return Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
                return Qt.AlignmentFlag.AlignCenter

            elif role == Qt.ItemDataRole.ForegroundRole and row in self._group_rows:
                return QBrush(QColor(0, 0, 139))

        return None

    def get_item_id(self, row):
        if 0 <= row < len(self._items_ids):
            return self._items_ids[row]
        return None

    def get_row_type(self, row):
        if 0 <= row < len(self._row_type):
            return self._row_type[row]
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]
        return None

    def is_group_row(self, row):
        return row in self._group_rows

    def delete_item(self, item_id):
        item = OtkazAgregateBase.get_by_id(item_id)
        item.delete_instance()


class UnTableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._data = []
        self._headers = []
        self._items_ids = []

    def load_data(self):
        """Method for data loading."""
        pass

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        row = index.row()
        col = index.column()

        if 0 <= row < self.rowCount() and 0 <= col < self.columnCount():
            if role == Qt.ItemDataRole.DisplayRole:
                return self._data[row][col]

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]
        return None

    def get_item_id(self, row):
        if 0 <= row < len(self._items_ids):
            return self._items_ids[row]
        return None

    def clear_data(self):
        self._data = []
        self._items_ids = []


class PlanesTypesModel(UnTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def load_data(self):
        self.beginResetModel()
        self.clear_data()
        self._headers = ["Наименование"]
        query = PlaneTypeBase.select()
        for data in query:
            self._data.append([data.name])
            self._items_ids.append([data.id])
        self.endResetModel()

    @staticmethod
    def delete_item(item_id):
        item = PlaneTypeBase.get_by_id(item_id)
        item.delete_instance()


class PodrazdModel(UnTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def load_data(self):
        self.beginResetModel()
        self.clear_data()
        self._headers = ["Наименование"]
        query = PodrazdBase.select()
        for data in query:
            self._data.append([data.name])
            self._items_ids.append([data.id])
        self.endResetModel()

    @staticmethod
    def delete_item(item_id):
        item = PodrazdBase.get_by_id(item_id)
        item.delete_instance()


class GroupModel(UnTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def load_data(self):
        self.beginResetModel()
        self.clear_data()
        self._headers = ["Группа", "Специальность", "Тип"]
        query = GroupBase.select()
        for data in query:
            self._data.append([data.name, data.spec.name, data.plane_type.name])
            self._items_ids.append([data.id])
        self.endResetModel()

    @staticmethod
    def delete_item(item_id):
        item = GroupBase.get_by_id(item_id)
        item.delete_instance()

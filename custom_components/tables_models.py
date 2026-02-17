from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt6.QtGui import QFont, QBrush, QColor

from data.data import TypeBase, PodrazdBase, GroupBase, OtkazAgregateBase, AgregateBase, SystemBase, PlaneBase, OsobBase


class IspravnostTableModel(QAbstractTableModel):
    def __init__(self, plane, parent=None):
        super().__init__(parent)
        self.plane = plane
        self._data = None
        self._headers = ["Наименование", "Система", "Номер агрегата/блока", "Снят", "Примечание"]
        self._prepared_data = []
        self._group_rows = []
        self._group_values = []
        self._row_type = []
        self.load_data()

    def load_data(self):
        self.beginResetModel()
        self._prepared_data = []
        self._group_rows = []
        self._group_values = []
        self._row_type = []
        self._data = (OtkazAgregateBase.select()
                                        .where(OtkazAgregateBase.plane == self.plane))
        sorted_data = sorted(self._data, key=lambda x: str(x.agregate.system.name))
        current_group = None
        row_idx = 0

        for item in sorted_data:
            group_value = str(item.agregate.system.group.name)
            if group_value != current_group:
                self._prepared_data.append([group_value] * (len(self._headers)))
                self._group_rows.append(row_idx)
                self._row_type.append('group')
                row_idx += 1
                current_group = group_value

            if item.removed:
                removed = 'Снят'
            else:
                removed = 'На самолете'
            row_data = [item, item.agregate.name, item.agregate.system.name, item.number, removed, item.description]
            self._prepared_data.append(row_data)
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
                value = self._prepared_data[row][col+1]
                return str(value) if value is not None else ""

            elif role == Qt.ItemDataRole.FontRole and row in self._group_rows:
                font = QFont()
                font.setBold(True)
                font.setPointSize(10)
                return font
            
            elif role == Qt.ItemDataRole.UserRole:
                if self._row_type[row] == 'agregate':
                    return self._prepared_data[row][0]
                return None

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

    def get_item(self, index):
        item = self.data(index, role=Qt.ItemDataRole.UserRole)
        return item

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

    @staticmethod
    def delete_item(item_id):
        item = OtkazAgregateBase.get_by_id(item_id)
        item.delete_instance()


class UnTableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._data = []
        self._headers = []
        self.load_data()

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
                return self._data[row][col+1]
            elif role == Qt.ItemDataRole.UserRole:
                return self._data[row][0]
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]
        return None

    def clear_data(self):
        self._data = []

    @staticmethod
    def delete_item(item):
        item.delete_instance()


class PlanesTypesModel(UnTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._headers = ["Наименование"]

    def load_data(self):
        self.beginResetModel()
        self.clear_data()
        query = TypeBase.select()
        for plane_type in list(query):
            self._data.append([plane_type, plane_type.name])
        self.endResetModel()


class PodrazdModel(UnTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._headers = ["Наименование"]

    def load_data(self):
        self.beginResetModel()
        self.clear_data()
        query = PodrazdBase.select()
        for data in query:
            self._data.append([data, data.name])
        self.endResetModel()


class GroupModel(UnTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._headers = ["Группа", "Тип"]

    def load_data(self, filter_str=None):
        self.beginResetModel()
        self.clear_data()
        query = GroupBase.select().join(TypeBase)
        if filter_str is not None:
            query = query.where(TypeBase.name == filter_str)
        for data in query:
            self._data.append([data, data.name, data.plane_type.name])
        self.endResetModel()


class SystemModel(UnTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._headers = ["Система", "Группа обслуживания", "Тип самолета"]

    def load_data(self, filter_str=None):
        pass


class AgregateModel(UnTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._headers = ["Блок/Агрегат", "Система", "Группа", "Тип самолета"]

    def load_data(self, filter_type=None, filter_group=None, filter_system=None):
        self.beginResetModel()
        query = (AgregateBase
                 .select()
                 .join(SystemBase)
                 .join(GroupBase)
                 .join(TypeBase)
                 )

        if filter_system:
            query = query.where(AgregateBase.system == filter_system)
        elif filter_group:
            query = query.where(AgregateBase.system.group == filter_group)
        elif filter_type:
            query = query.where(AgregateBase.system.plane_type == filter_type)
        self.clear_data()
        for agregate in query:
            self._data.append([agregate,
                               agregate.name,
                               agregate.system.name,
                               agregate.system.group.name,
                               agregate.system.plane_type.name])
        self.endResetModel()


class PlanesModel(UnTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def load_data(self, filter_type=None, filter_group=None, filter_system=None):
        self.beginResetModel()
        self.clear_data()
        self._headers = ["Тип самолета", "Подразделение", "Бортовой номер"]

        if filter_type:
            query = (PlaneBase.select()
                     .where(PlaneBase.plane_type == filter_type))
        else:
            query = PlaneBase.select()

        for data in query:
            self._data.append([data, data.plane_type.name, data.podrazd.name, data.bort_number])
        self.endResetModel()


class OsobModel(UnTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def load_data(self, filter_type=None):
        self.beginResetModel()
        self.clear_data()
        self._headers = ['Тип самолета', 'Особенности']
        if filter_type:
            query = (OsobBase
                     .select()
                     .where(OsobBase.plane_type == filter_type))
        else:
            query = OsobBase.select()

        for data in query:
            self._data.append([data.plane_type, data.name])
        self.endResetModel()

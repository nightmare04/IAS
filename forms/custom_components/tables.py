from PyQt6.QtCore import Qt, QModelIndex, QAbstractTableModel
from PyQt6.QtGui import QBrush, QColor, QFont
from PyQt6.QtWidgets import QTableView, QAbstractItemView, QSizePolicy, QHeaderView, QDialog, QMessageBox

from data import PlaneBase, OtkazAgregateBase
from forms.otkaz_dialog import EditOtkazDialog


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
                self._prepared_data.append([''] * (len(self._headers)))
                self._group_rows.append(row_idx)
                self._group_values.append(group_value)
                self._items_ids.append(None)
                self._row_type.append('group')
                row_idx += 1
                current_group = group_value

            # Добавляем обычную строку данных
            row_data = [item.agregate.name, item.agregate.system.name, item.number, '']
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
                if row in self._group_rows:
                    if col == 0:
                        group_index = self._group_rows.index(row)
                        return self._group_values[group_index]
                    return ""
                else:
                    value = self._prepared_data[row][col]
                    return str(value) if value is not None else ""

            elif role == Qt.ItemDataRole.FontRole and row in self._group_rows:
                font = QFont()
                font.setBold(True)
                font.setPointSize(10)
                return font

            elif role == Qt.ItemDataRole.BackgroundRole and row in self._group_rows:
                return QBrush(QColor(220, 220, 220))

            elif role == Qt.ItemDataRole.TextAlignmentRole and row in self._group_rows:
                if col == 0:
                    return Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
                return Qt.AlignmentFlag.AlignCenter

            elif role == Qt.ItemDataRole.ForegroundRole and row in self._group_rows:
                return QBrush(QColor(0, 0, 139))  # Темно-синий цвет для групп

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


class IspravnostTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def setSpanForGroups(self):
        model = self.model()
        if isinstance(model, IspravnostTableModel):
            for row in range(model.rowCount()):
                if model.is_group_row(row):
                    self.setSpan(row, 0, 1, model.columnCount())

    def edit_item(self, item_id):
        try:
            item = OtkazAgregateBase.get(OtkazAgregateBase.id == item_id)
            dialog = EditOtkazDialog(item)
            dialog.exec()

        except OtkazAgregateBase.DoesNotExist:
            QMessageBox.warning(self, "Ошибка", "Блок/агрегат не найден!")
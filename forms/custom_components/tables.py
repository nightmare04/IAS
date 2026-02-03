from PyQt6.QtCore import Qt, QModelIndex, QAbstractTableModel
from PyQt6.QtGui import QBrush, QColor, QFont, QAction
from PyQt6.QtWidgets import QTableView, QAbstractItemView, QSizePolicy, QHeaderView, QMessageBox, QMenu

from data import  OtkazAgregateBase
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


class IspravnostTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

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
                    self.setSpan(row, col, 1, 1)

    def edit_item(self, item_id):
        try:
            item = OtkazAgregateBase.get_by_id(item_id)
            dialog = EditOtkazDialog(item)
            dialog.exec()

        except OtkazAgregateBase.DoesNotExist:
            QMessageBox.warning(self, "Ошибка", "Блок/агрегат не найден!")

    def delete_item(self, item_id):
        parent = self.parent()
        item = OtkazAgregateBase.get_by_id(item_id)
        item.delete_instance()
        parent.refresh_data()


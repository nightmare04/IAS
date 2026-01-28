from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt6.QtGui import QFont, QBrush, QColor
from PyQt6.QtWidgets import QTableView, QAbstractItemView


class GroupTableModel(QAbstractTableModel):
    def __init__(self, data, headers, parent=None):
        super().__init__(parent)
        self._headers = headers[1:]  # Исключаем первый заголовок
        self._raw_data = data
        self._prepared_data = []
        self._group_rows = []  # Индексы строк с группами
        self._group_values = []  # Значения групп
        self._prepare_data()

    def _prepare_data(self):
        """Подготавливает данные с группами"""
        # Сортируем по первому столбцу для группировки
        sorted_data = sorted(self._raw_data, key=lambda x: str(x[0]))

        current_group = None
        row_idx = 0

        for row in sorted_data:
            group_value = str(row[0])

            # Если началась новая группа
            if group_value != current_group:
                # Добавляем строку группы
                self._prepared_data.append([''] * (len(self._headers)))  # Пустая строка для группы
                self._group_rows.append(row_idx)
                self._group_values.append(group_value)
                row_idx += 1
                current_group = group_value

            # Добавляем обычную строку данных без первого столбца
            self._prepared_data.append(row[1:])  # Исключаем первый элемент
            row_idx += 1

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
                    # Для строк групп показываем значение группы в первой колонке
                    if col == 0:
                        group_index = self._group_rows.index(row)
                        return self._group_values[group_index]
                    return ""  # Пустая строка для остальных колонок
                else:
                    # Для обычных строк
                    value = self._prepared_data[row][col]
                    return str(value) if value is not None else ""

            elif role == Qt.ItemDataRole.FontRole and row in self._group_rows:
                font = QFont()
                font.setBold(True)
                font.setPointSize(10)
                return font

            elif role == Qt.ItemDataRole.BackgroundRole and row in self._group_rows:
                return QBrush(QColor(220, 220, 220))  # Светло-серый фон для групп

            elif role == Qt.ItemDataRole.TextAlignmentRole and row in self._group_rows:
                if col == 0:
                    return Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
                return Qt.AlignmentFlag.AlignCenter

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]
        return None

    def isGroupRow(self, row):
        """Проверяет, является ли строка строкой группы"""
        return row in self._group_rows

    def getGroupValue(self, row):
        """Возвращает значение группы для строки"""
        if row in self._group_rows:
            index = self._group_rows.index(row)
            return self._group_values[index]
        return None


class GroupingTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

    def setSpanForGroups(self):
        """Объединяет ячейки для строк групп"""
        model = self.model()
        if isinstance(model, GroupTableModel):
            for row in range(model.rowCount()):
                if model.isGroupRow(row):
                    # Объединяем все ячейки в строке группы
                    self.setSpan(row, 0, 1, model.columnCount())
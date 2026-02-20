"""Table view for aircraft serviceability data."""
from typing import Any

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt, QTimer
from PyQt6.QtGui import QBrush, QColor, QFont

from data.models.aircraft import PlaneBase
from data.models.failures import OtkazAgregateBase

from .base_table import UnTableView


class IspravnostTableModel(QAbstractTableModel):
    """Table model for aircraft serviceability data with grouping."""

    HEADERS: list[str] = [
        "Наименование",
        "Система",
        "Номер агрегата/блока",
        "Снят",
        "Примечание",
    ]

    GROUP_BG_COLOR = QColor(220, 220, 220)
    GROUP_FG_COLOR = QColor(0, 0, 139)
    ROW_BG_COLOR = QColor(255, 255, 255)

    def __init__(self, plane: PlaneBase, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.plane = plane
        self._data: list[Any] = []
        self._prepared_data: list[list[Any]] = []
        self._group_rows: set[int] = set()
        self._row_type: list[str] = []
        self.load_data()

    def load_data(self) -> None:
        """Load failure data for the aircraft."""
        self.beginResetModel()
        self._prepared_data = []
        self._group_rows = set()
        self._row_type = []

        self._data = (OtkazAgregateBase
                      .select()
                      .where(OtkazAgregateBase.plane == self.plane)
                      .order_by(OtkazAgregateBase.agregate.system.name))

        current_group: str | None = None

        for item in self._data:
            group_value = str(item.agregate.system.group.name)
            if group_value != current_group:
                self._add_group_row(group_value)
                current_group = group_value

            self._add_agregate_row(item)

        self.endResetModel()

    def _add_group_row(self, group_name: str) -> None:
        """Add a group header row."""
        row_idx = len(self._prepared_data)
        self._prepared_data.append([group_name] * len(self.HEADERS))
        self._group_rows.add(row_idx)
        self._row_type.append("group")

    def _add_agregate_row(self, item: Any) -> None:
        """Add an aggregate data row."""
        removed = "Снят" if item.removed else "На самолете"
        row_data = [
            item,
            item.agregate.name,
            item.agregate.system.name,
            item.number,
            removed,
            item.description,
        ]
        self._prepared_data.append(row_data)
        self._row_type.append("agregate")

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Return number of rows."""
        return len(self._prepared_data)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Return number of columns."""
        return len(self.HEADERS)

    def data(self, index: QModelIndex, role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole) -> Any:
        """Return data for the given index and role."""
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()

        if not (0 <= row < len(self._prepared_data) and 0 <= col < len(self.HEADERS)):
            return None

        is_group = row in self._group_rows

        if role == Qt.ItemDataRole.DisplayRole:
            value = self._prepared_data[row][col + 1]
            return str(value) if value is not None else ""

        if role == Qt.ItemDataRole.FontRole and is_group:
            font = QFont()
            font.setBold(True)
            font.setPointSize(10)
            return font

        if role == Qt.ItemDataRole.UserRole:
            return self._prepared_data[row][0] if self._row_type[row] == "agregate" else None

        if role == Qt.ItemDataRole.BackgroundRole:
            return QBrush(self.GROUP_BG_COLOR if is_group else self.ROW_BG_COLOR)

        if role == Qt.ItemDataRole.TextAlignmentRole and is_group:
            if col == 0:
                return Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
            return Qt.AlignmentFlag.AlignCenter

        if role == Qt.ItemDataRole.ForegroundRole and is_group:
            return QBrush(self.GROUP_FG_COLOR)

        return None

    def get_item(self, index: QModelIndex) -> Any:
        """Get item at index."""
        return self.data(index, role=Qt.ItemDataRole.UserRole)

    def get_row_type(self, row: int) -> str | None:
        """Get row type (group or agregate)."""
        if 0 <= row < len(self._row_type):
            return self._row_type[row]
        return None

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole
    ) -> Any:
        """Return header data."""
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]
        return None

    @staticmethod
    def delete_item(item: Any) -> None:
        """Delete item from database."""
        item.delete_instance()


class IspravnostTable(UnTableView):
    """Table view for aircraft serviceability data."""

    def __init__(self, plane: PlaneBase, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.table_model = IspravnostTableModel(plane)
        self.setModel(self.table_model)

    def set_span_for_groups(self) -> None:
        """Set row spans for group rows."""
        self.clear_all_span()
        if isinstance(self.table_model, IspravnostTableModel):
            for row in range(self.table_model.rowCount()):
                if self.table_model.get_row_type(row) == 'group':
                    self.setSpan(row, 0, 1, self.table_model.columnCount())

    def clear_all_span(self) -> None:
        """Clear all row spans."""
        if isinstance(self.table_model, IspravnostTableModel):
            rows = self.table_model.rowCount()
            cols = self.table_model.columnCount()
            for row in range(rows):
                for col in range(cols):
                    if self.rowSpan(row, col) > 1:
                        self.setSpan(row, col, 1, 1)

    def set_filter(self, filter_text: str) -> None:
        """Set filter for table data."""
        pass

    def load_data(self) -> None:
        """Load data from database."""
        self.table_model.load_data()
        self.clear_all_span()
        QTimer.singleShot(0, self.set_span_for_groups)

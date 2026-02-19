"""Table models for displaying data in IAS application."""
from typing import Any

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt6.QtGui import QBrush, QColor, QFont

from app.models.aircraft import (
    AgregateBase,
    GroupBase,
    PlaneBase,
    PodrazdBase,
    SystemBase,
    TypeBase,
)
from app.models.failures import OtkazAgregateBase
from app.models.osob import OsobBase


class TableModel(QAbstractTableModel):
    HEADERS: list[str] = []

    def __init__(self, data_model, parent=None, **kwargs) -> None:
        super().__init__(parent)
        self.data_model = data_model
        self.filter_args = {}
        self.filter_args.update(kwargs)
        self._data = data_model.select()

    def _filter_data(self):
        if self.filter_args.get('plane_type') is not None:
            self._data = self._data.where(self.data_model.plane_type == self.filter_args.get('plane_type'))


class UnTableModel(QAbstractTableModel):
    """Base table model with common functionality."""

    HEADERS: list[str] = []

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self._data: list[list[Any]] = []
        self.load_data()

    def load_data(self) -> None:
        """Load data from database. Override in subclasses."""
        pass

    def rowCount(self, parent: Any | None = None) -> int:
        """Return number of rows."""
        return len(self._data)

    def columnCount(self, parent: Any | None = None) -> int:
        """Return number of columns."""
        return len(self.HEADERS)

    def data(self, index: Any, role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole) -> Any:
        """Return data for the given index and role."""
        if not index.isValid():
            return None
        row = index.row()
        col = index.column()

        if 0 <= row < self.rowCount() and 0 <= col < self.columnCount():
            if role == Qt.ItemDataRole.DisplayRole:
                return self._data[row][col + 1]
            elif role == Qt.ItemDataRole.UserRole:
                return self._data[row][0]
        return None

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole
    ) -> Any:
        """Return header data."""
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]
        return None

    def clear_data(self) -> None:
        """Clear all data."""
        self._data = []

    @staticmethod
    def delete_item(item: Any) -> None:
        """Delete item from database."""
        item.delete_instance()


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


class PlanesTypesModel(UnTableModel):
    """Table model for aircraft types."""
    HEADERS: list[str] = [
        "Наименование",
    ]

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)

    def load_data(self) -> None:
        """Load aircraft types."""
        self.beginResetModel()
        self.clear_data()
        query = TypeBase.select()
        for plane_type in list(query):
            self._data.append([plane_type, plane_type.name])
        self.endResetModel()


class PodrazdModel(UnTableModel):
    """Table model for divisions."""
    HEADERS: list[str] = [
        "Наименование",
    ]

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)

    def load_data(self) -> None:
        """Load divisions."""
        self.beginResetModel()
        self.clear_data()
        query = PodrazdBase.select()
        for data in query:
            self._data.append([data, data.name])
        self.endResetModel()


class GroupModel(UnTableModel):
    """Table model for maintenance groups."""
    HEADERS: list[str] = [
        "Группа",
        "Тип"
    ]

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)

    def load_data(self, filter_str: str | None = None) -> None:
        """Load maintenance groups with optional filter."""
        self.beginResetModel()
        self.clear_data()
        query = GroupBase.select().join(TypeBase)
        if filter_str is not None:
            query = query.where(TypeBase.name == filter_str)
        for data in query:
            self._data.append([data, data.name, data.plane_type.name])
        self.endResetModel()


class SystemModel(UnTableModel):
    """Table model for aircraft systems."""
    HEADERS: list[str] = [
        "Система",
        "Группа обслуживания",
        "Тип самолета"
    ]

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)

    def load_data(self, filter_str: str | None = None) -> None:
        """Load systems with optional filter."""
        self.beginResetModel()
        self.clear_data()
        query = SystemBase.select().join(GroupBase).join(TypeBase)
        if filter_str is not None:
            query = query.where(TypeBase.name == filter_str)
        for data in query:
            self._data.append([data, data.name, data.group.name, data.plane_type.name])
        self.endResetModel()


class AgregateModel(UnTableModel):
    """Table model for aggregates/units."""

    HEADERS: list[str] = [
        "Блок/Агрегат",
        "Система",
        "Группа",
        "Тип самолета"
    ]

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)

    def load_data(
        self,
        filter_type: Any | None = None,
        filter_group: Any | None = None,
        filter_system: Any | None = None,
    ) -> None:
        """Load aggregates with optional filters."""
        self.beginResetModel()
        query = (
            AgregateBase.select()
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
            self._data.append(
                [
                    agregate,
                    agregate.name,
                    agregate.system.name,
                    agregate.system.group.name,
                    agregate.system.plane_type.name,
                ]
            )
        self.endResetModel()


class PlanesModel(UnTableModel):
    """Table model for aircraft."""

    HEADERS: list[str] = [
        "Тип самолета",
        "Подразделение",
        "Бортовой номер",
    ]

    def __init__(self, parent: Any | None = None) -> None:
        self.filter: dict[str, Any] = {}
        super().__init__(parent)

    def set_filter(self, filter_dict: dict[str, Any]) -> None:
        """Set filter for aircraft list."""
        self.filter = filter_dict
        self.load_data()

    def load_data(self) -> None:
        """Load aircraft with optional filters."""
        self.beginResetModel()
        self.clear_data()
        query = PlaneBase.select()

        if isinstance(self.filter.get("plane_type"), TypeBase):
            query = query.where(PlaneBase.plane_type == self.filter["plane_type"])

        if isinstance(self.filter.get("podrazd"), PodrazdBase):
            query = query.where(PlaneBase.podrazd == self.filter["podrazd"])

        for data in query:
            self._data.append(
                [data, data.plane_type.name, data.podrazd.name, data.bort_number]
            )
        self.endResetModel()


class OsobModel(UnTableModel):
    """Table model for aircraft features."""

    HEADERS: list[str] = [
        "Тип самолета",
        "Особенности",
    ]

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)

    def load_data(self, filter_type: Any | None = None) -> None:
        """Load features with optional filter."""
        self.beginResetModel()
        self.clear_data()
        self._headers = ["Тип самолета", "Особенности"]
        if filter_type:
            query = OsobBase.select().where(OsobBase.plane_type == filter_type)
        else:
            query = OsobBase.select()

        for data in query:
            self._data.append([data.plane_type, data.name])
        self.endResetModel()

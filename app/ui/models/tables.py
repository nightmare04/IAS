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


class IspravnostTableModel(QAbstractTableModel):
    """Table model for aircraft serviceability data with grouping."""

    def __init__(self, plane: PlaneBase, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.plane = plane
        self._data: list[Any] = []
        self._headers: list[str] = [
            "Наименование",
            "Система",
            "Номер агрегата/блока",
            "Снят",
            "Примечание",
        ]
        self._prepared_data: list[list[Any]] = []
        self._group_rows: list[int] = []
        self._group_values: list[Any] = []
        self._row_type: list[str] = []
        self.load_data()

    def load_data(self) -> None:
        """Load failure data for the aircraft."""
        self.beginResetModel()
        self._prepared_data = []
        self._group_rows = []
        self._group_values = []
        self._row_type = []

        self._data = OtkazAgregateBase.select().where(OtkazAgregateBase.plane == self.plane)
        sorted_data = sorted(self._data, key=lambda x: str(x.agregate.system.name))

        current_group: str | None = None
        row_idx = 0

        for item in sorted_data:
            group_value = str(item.agregate.system.group.name)
            if group_value != current_group:
                self._prepared_data.append([group_value] * len(self._headers))
                self._group_rows.append(row_idx)
                self._row_type.append("group")
                row_idx += 1
                current_group = group_value

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
            row_idx += 1

        self.endResetModel()

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Return number of rows."""
        return len(self._prepared_data)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Return number of columns."""
        return len(self._headers)

    def data(self, index: QModelIndex, role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole) -> Any:
        """Return data for the given index and role."""
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()

        if 0 <= row < len(self._prepared_data) and 0 <= col < len(self._headers):
            if role == Qt.ItemDataRole.DisplayRole:
                value = self._prepared_data[row][col + 1]
                return str(value) if value is not None else ""

            elif role == Qt.ItemDataRole.FontRole and row in self._group_rows:
                font = QFont()
                font.setBold(True)
                font.setPointSize(10)
                return font

            elif role == Qt.ItemDataRole.UserRole:
                if self._row_type[row] == "agregate":
                    return self._prepared_data[row][0]
                return None

            elif role == Qt.ItemDataRole.BackgroundRole:
                if self._row_type[row] == "group":
                    return QBrush(QColor(220, 220, 220))
                return QBrush(QColor(255, 255, 255))

            elif role == Qt.ItemDataRole.TextAlignmentRole and row in self._group_rows:
                if col == 0:
                    return Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
                return Qt.AlignmentFlag.AlignCenter

            elif role == Qt.ItemDataRole.ForegroundRole and row in self._group_rows:
                return QBrush(QColor(0, 0, 139))

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
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]
        return None

    def is_group_row(self, row: int) -> bool:
        """Check if row is a group header row."""
        return row in self._group_rows

    @staticmethod
    def delete_item(item: Any) -> None:
        """Delete item from database."""
        item.delete_instance()


class UnTableModel(QAbstractTableModel):
    """Base table model with common functionality."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self._data: list[list[Any]] = []
        self._headers: list[str] = []
        self.load_data()

    def load_data(self) -> None:
        """Load data from database. Override in subclasses."""
        pass

    def rowCount(self, parent: Any | None = None) -> int:
        """Return number of rows."""
        return len(self._data)

    def columnCount(self, parent: Any | None = None) -> int:
        """Return number of columns."""
        return len(self._headers)

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
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]
        return None

    def clear_data(self) -> None:
        """Clear all data."""
        self._data = []

    @staticmethod
    def delete_item(item: Any) -> None:
        """Delete item from database."""
        item.delete_instance()


class PlanesTypesModel(UnTableModel):
    """Table model for aircraft types."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self._headers = ["Наименование"]

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

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self._headers = ["Наименование"]

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

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self._headers = ["Группа", "Тип"]

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

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self._headers = ["Система", "Группа обслуживания", "Тип самолета"]

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

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self._headers = ["Блок/Агрегат", "Система", "Группа", "Тип самолета"]

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
        self._headers = ["Тип самолета", "Подразделение", "Бортовой номер"]

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

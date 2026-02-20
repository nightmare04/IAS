"""Custom combo boxes for IAS application."""
from typing import Any

from PyQt6.QtCore import QAbstractListModel, Qt, pyqtSignal
from PyQt6.QtWidgets import QComboBox

from data.models.aircraft import AgregateBase, GroupBase, PodrazdBase, SystemBase, TypeBase


class ComboBoxModel(QAbstractListModel):
    """Model for combo boxes with Peewee ORM integration."""

    def __init__(
        self,
        peewee_model: type | None = None,
        first_string: str | None = None,
        display_field: str = "name",
        parent: Any | None = None,
    ) -> None:
        super().__init__(parent)
        self._peewee_model = peewee_model
        self._first_string = first_string
        self.display_field = display_field
        self.filter: dict[str, Any] = {}
        self._data: list[Any] = []
        self._custom_data: list[Any] | None = None  # For custom data lists
        self.load_data()

    def set_custom_data(self, data: list[Any]) -> None:
        """Set custom data list (for filtered by features)."""
        self._custom_data = data
        self.load_data()

    def get_filtered_query(self) -> Any:
        """Get filtered query based on current filters."""
        if self._peewee_model is None:
            return []

        # If custom data is set, use it directly
        if self._custom_data is not None:
            return self._custom_data

        query = self._peewee_model.select()
        for key, value in self.filter.items():
            # Extract ID if value is a model instance
            filter_value = value.id if hasattr(value, 'id') else value
            query = query.where(getattr(self._peewee_model, key) == filter_value)
        return query

    def load_data(self) -> None:
        """Load data from database."""
        self._data = []
        query = self.get_filtered_query()
        self._data = list(query)
        if self._first_string:
            self._data.insert(0, self._first_string)

    def rowCount(self, parent: Any | None = None) -> int:
        """Return number of rows."""
        return len(self._data)

    def data(self, index: Any, role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole) -> Any:
        """Return data for the given index and role."""
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

    def refresh(self) -> None:
        """Refresh data from database."""
        self.beginResetModel()
        self.load_data()
        self.endResetModel()


class IASComboBox(QComboBox):
    """Base combo box with custom signal."""

    changed = pyqtSignal(object)

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.currentIndexChanged.connect(self.emit_changed)

    def emit_changed(self, index: int) -> None:
        """Emit changed signal with selected item."""
        item = self.itemData(index, role=Qt.ItemDataRole.UserRole)
        self.changed.emit(item)

    def set_filter(self) -> None:
        """Set filter for the combo box model."""
        pass


class PlaneTypeComboBox(IASComboBox):
    """Combo box for aircraft types."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self._model = ComboBoxModel(
            peewee_model=TypeBase, first_string="Выберите тип самолета"
        )
        self.setModel(self._model)


class PodrazdComboBox(IASComboBox):
    """Combo box for divisions."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self._model = ComboBoxModel(
            peewee_model=PodrazdBase, first_string="Выберите подразделение"
        )
        self.setModel(self._model)


class GroupComboBox(IASComboBox):
    """Combo box for maintenance groups."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self._model = ComboBoxModel(
            peewee_model=GroupBase, first_string="Выберите группу обслуживания"
        )
        self.setModel(self._model)

    def set_filter(self, plane_type: TypeBase) -> None:
        """Filter by aircraft type."""
        self._model.filter = {"plane_type": plane_type}
        self._model.load_data()
        # Reset to first real item (not the placeholder)
        if self.count() > 1:
            self.setCurrentIndex(1)
        elif self.count() > 0:
            self.setCurrentIndex(0)


class SystemComboBox(IASComboBox):
    """Combo box for aircraft systems."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self._model = ComboBoxModel(
            peewee_model=SystemBase, first_string="Выберите систему самолета"
        )
        self.setModel(self._model)

    def set_filter(self, group: GroupBase) -> None:
        """Filter by maintenance group."""
        self._model.filter = {"group": group}
        self._model.load_data()
        # Reset to first real item (not the placeholder)
        if self.count() > 1:
            self.setCurrentIndex(1)
        elif self.count() > 0:
            self.setCurrentIndex(0)


class AgregateComboBox(IASComboBox):
    """Combo box for aggregates/units."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self._model = ComboBoxModel(
            peewee_model=AgregateBase, first_string="Выберите блок/агрегат самолета"
        )
        self.setModel(self._model)

    def set_filter(self, system: SystemBase) -> None:
        """Filter by system."""
        self._model.filter = {"system": system}
        self._model.load_data()
        # Reset to first real item (not the placeholder)
        if self.count() > 1:
            self.setCurrentIndex(1)
        elif self.count() > 0:
            self.setCurrentIndex(0)

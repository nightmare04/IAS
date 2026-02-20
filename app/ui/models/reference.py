"""Reference table models for IAS application."""
from typing import Any

from app.models.aircraft import (
    AgregateBase,
    GroupBase,
    PlaneBase,
    PodrazdBase,
    SystemBase,
    TypeBase,
)
from app.models.osob import OsobBase

from .base import UnTableModel


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

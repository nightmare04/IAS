"""Tests for table models."""
import pytest
from PyQt6.QtCore import QModelIndex, Qt

from data.models.aircraft import TypeBase, PodrazdBase, GroupBase, PlaneBase
from app.ui.widgets.tables import (
    PlanesTypesModel,
    PodrazdModel,
    GroupModel,
    PlanesModel,
)


class TestPlanesTypesModel:
    """Tests for PlanesTypesModel."""

    def test_load_data(self, qtbot) -> None:
        """Test loading aircraft types."""
        # Create test data
        TypeBase.create(name="Test Type 1")
        TypeBase.create(name="Test Type 2")

        model = PlanesTypesModel()
        qtbot.waitUntil(lambda: model.rowCount() >= 2, timeout=1000)

        assert model.rowCount() >= 2
        assert model.columnCount() == 1

    def test_header_data(self, qtbot) -> None:
        """Test header data."""
        model = PlanesTypesModel()
        header = model.headerData(0, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)
        assert header == "Наименование"


class TestPodrazdModel:
    """Tests for PodrazdModel."""

    def test_load_data(self, qtbot) -> None:
        """Test loading divisions."""
        PodrazdBase.create(name="Division 1")
        PodrazdBase.create(name="Division 2")

        model = PodrazdModel()
        qtbot.waitUntil(lambda: model.rowCount() >= 2, timeout=1000)

        assert model.rowCount() >= 2


class TestGroupModel:
    """Tests for GroupModel."""

    def test_load_data_with_filter(self, qtbot) -> None:
        """Test loading groups with filter."""
        plane_type = TypeBase.create(name="Filter Test Type")
        GroupBase.create(name="Group 1", plane_type=plane_type)
        GroupBase.create(name="Group 2", plane_type=plane_type)

        model = GroupModel()
        model.load_data("Filter Test Type")

        qtbot.waitUntil(lambda: model.rowCount() >= 2, timeout=1000)
        assert model.rowCount() >= 2

    def test_load_data_filtered(self, qtbot) -> None:
        """Test loading groups with specific filter."""
        type1 = TypeBase.create(name="Type A")
        type2 = TypeBase.create(name="Type B")
        GroupBase.create(name="Group A", plane_type=type1)
        GroupBase.create(name="Group B", plane_type=type2)

        model = GroupModel()
        model.load_data("Type A")

        qtbot.waitUntil(lambda: model.rowCount() >= 1, timeout=1000)
        assert model.rowCount() >= 1


class TestPlanesModel:
    """Tests for PlanesModel."""

    def test_load_data(self, qtbot) -> None:
        """Test loading aircraft."""
        plane_type = TypeBase.create(name="Plane Type")
        podrazd = PodrazdBase.create(name="Podrazd")
        PlaneBase.create(plane_type=plane_type, podrazd=podrazd, zav_num="001", bort_number="01")

        model = PlanesModel()
        qtbot.waitUntil(lambda: model.rowCount() >= 1, timeout=1000)

        assert model.rowCount() >= 1

    def test_set_filter(self, qtbot) -> None:
        """Test filtering aircraft."""
        type1 = TypeBase.create(name="Type 1")
        type2 = TypeBase.create(name="Type 2")
        podrazd = PodrazdBase.create(name="Podrazd")

        PlaneBase.create(plane_type=type1, podrazd=podrazd, zav_num="001", bort_number="01")
        PlaneBase.create(plane_type=type2, podrazd=podrazd, zav_num="002", bort_number="02")

        model = PlanesModel()
        model.set_filter({"plane_type": type1})

        qtbot.waitUntil(lambda: model.rowCount() == 1, timeout=1000)
        assert model.rowCount() == 1

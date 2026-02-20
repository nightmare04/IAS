"""Tests for Peewee models."""
import pytest
from peewee import IntegrityError

from data.models.aircraft import TypeBase, PodrazdBase, GroupBase, SystemBase, AgregateBase, PlaneBase
from data.models.failures import OtkazAgregateBase


class TestTypeBase:
    """Tests for TypeBase model."""

    def test_create_type(self) -> None:
        """Test creating aircraft type."""
        plane_type = TypeBase.create(name="Test Type")
        assert plane_type.id is not None
        assert plane_type.name == "Test Type"

    def test_unique_constraint(self) -> None:
        """Test unique constraint on name."""
        TypeBase.create(name="Unique Type")
        with pytest.raises(IntegrityError):
            TypeBase.create(name="Unique Type")


class TestPodrazdBase:
    """Tests for PodrazdBase model."""

    def test_create_podrazd(self) -> None:
        """Test creating division."""
        podrazd = PodrazdBase.create(name="Test Division")
        assert podrazd.id is not None
        assert podrazd.name == "Test Division"


class TestGroupBase:
    """Tests for GroupBase model."""

    def test_create_group(self) -> None:
        """Test creating maintenance group."""
        plane_type = TypeBase.create(name="Group Type")
        group = GroupBase.create(name="Test Group", plane_type=plane_type)
        assert group.id is not None
        assert group.name == "Test Group"
        assert group.plane_type == plane_type

    def test_cascade_delete(self) -> None:
        """Test cascade delete on plane type."""
        plane_type = TypeBase.create(name="Cascade Type")
        group = GroupBase.create(name="Cascade Group", plane_type=plane_type)
        group_id = group.id

        plane_type.delete_instance()

        with pytest.raises(GroupBase.DoesNotExist):
            GroupBase.get_by_id(group_id)


class TestPlaneBase:
    """Tests for PlaneBase model."""

    def test_create_plane(self) -> None:
        """Test creating aircraft."""
        plane_type = TypeBase.create(name="Plane Type")
        podrazd = PodrazdBase.create(name="Plane Podrazd")
        plane = PlaneBase.create(
            plane_type=plane_type,
            podrazd=podrazd,
            zav_num="12345",
            bort_number="01",
        )
        assert plane.id is not None
        assert plane.zav_num == "12345"
        assert plane.bort_number == "01"

    def test_unique_zav_num(self) -> None:
        """Test unique constraint on zav_num."""
        plane_type = TypeBase.create(name="Zav Type")
        podrazd = PodrazdBase.create(name="Zav Podrazd")
        PlaneBase.create(plane_type=plane_type, podrazd=podrazd, zav_num="UNIQUE", bort_number="01")

        with pytest.raises(IntegrityError):
            PlaneBase.create(plane_type=plane_type, podrazd=podrazd, zav_num="UNIQUE", bort_number="02")


class TestOtkazAgregateBase:
    """Tests for OtkazAgregateBase model."""

    def test_create_failure(self) -> None:
        """Test creating failure record."""
        plane_type = TypeBase.create(name="Failure Type")
        podrazd = PodrazdBase.create(name="Failure Podrazd")
        group = GroupBase.create(name="Failure Group", plane_type=plane_type)
        system = SystemBase.create(name="Failure System", group=group, plane_type=plane_type)
        agregate = AgregateBase.create(name="Failure Agregate", system=system)
        plane = PlaneBase.create(plane_type=plane_type, podrazd=podrazd, zav_num="FAIL001", bort_number="01")

        failure = OtkazAgregateBase.create(
            agregate=agregate,
            plane=plane,
            number="123",
            description="Test failure",
            removed=False,
        )

        assert failure.id is not None
        assert failure.number == "123"
        assert failure.description == "Test failure"
        assert failure.removed is False

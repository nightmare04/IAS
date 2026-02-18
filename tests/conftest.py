"""Pytest configuration and fixtures."""
import pytest
from peewee import SqliteDatabase

from app.database import get_database
from app.models import (
    TypeBase,
    PodrazdBase,
    GroupBase,
    SystemBase,
    AgregateBase,
    PlaneBase,
    OsobBase,
    OsobPlaneBase,
    OsobSystemAddBase,
    OsobSystemRemoveBase,
    OsobAgregateAddBase,
    OsobAgregateRemoveBase,
    OtkazAgregateBase,
)


TEST_DATABASE = SqliteDatabase(":memory:", pragmas={"foreign_keys": 1})


@pytest.fixture(scope="session")
def test_db():
    """Create test database and tables."""
    TEST_DATABASE.bind(
        [
            TypeBase,
            PodrazdBase,
            GroupBase,
            SystemBase,
            AgregateBase,
            PlaneBase,
            OsobBase,
            OsobPlaneBase,
            OsobSystemAddBase,
            OsobSystemRemoveBase,
            OsobAgregateAddBase,
            OsobAgregateRemoveBase,
            OtkazAgregateBase,
        ],
        bind_refs=False,
        bind_backrefs=False,
    )
    TEST_DATABASE.create_tables(
        [
            TypeBase,
            PodrazdBase,
            GroupBase,
            SystemBase,
            AgregateBase,
            PlaneBase,
            OsobBase,
            OsobPlaneBase,
            OsobSystemAddBase,
            OsobSystemRemoveBase,
            OsobAgregateAddBase,
            OsobAgregateRemoveBase,
            OtkazAgregateBase,
        ],
        safe=True,
    )
    yield TEST_DATABASE
    TEST_DATABASE.drop_tables(
        [
            TypeBase,
            PodrazdBase,
            GroupBase,
            SystemBase,
            AgregateBase,
            PlaneBase,
            OsobBase,
            OsobPlaneBase,
            OsobSystemAddBase,
            OsobSystemRemoveBase,
            OsobAgregateAddBase,
            OsobAgregateRemoveBase,
            OtkazAgregateBase,
        ],
        safe=True,
    )


@pytest.fixture(autouse=True)
def clean_database(test_db):
    """Clean database before each test."""
    # Clear all tables before each test
    tables = [
        OtkazAgregateBase,
        OsobAgregateRemoveBase,
        OsobAgregateAddBase,
        OsobSystemRemoveBase,
        OsobSystemAddBase,
        OsobPlaneBase,
        OsobBase,
        PlaneBase,
        AgregateBase,
        SystemBase,
        GroupBase,
        PodrazdBase,
        TypeBase,
    ]
    for table in tables:
        table.delete().execute()
    yield test_db

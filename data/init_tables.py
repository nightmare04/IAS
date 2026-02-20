"""Legacy init_tables module - backward compatibility."""
from app.database import get_database, run_migrations
from data.models import (
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

db = get_database()


def create_tables() -> None:
    """Create all database tables via migrations."""
    run_migrations()


def drop_tables() -> None:
    """Drop all tables - USE WITH CAUTION."""
    db.drop_tables(
        [
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
        ],
        safe=True,
    )


def fill_tables() -> None:
    """Fill tables with example data.
    
    Note: Example data functionality has been removed.
    Implement your own data seeding logic here if needed.
    """
    pass


__all__ = ["create_tables", "drop_tables", "fill_tables", "db"]

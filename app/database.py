"""
Database connection and migration utilities.
"""
from peewee import SqliteDatabase
from peewee_migrate import Router

from app.config import DATABASE_NAME, MIGRATIONS_DIR


def get_database() -> SqliteDatabase:
    """Get database instance with foreign keys enabled."""
    return SqliteDatabase(DATABASE_NAME, pragmas={"foreign_keys": 1})


def get_router(database: SqliteDatabase | None = None) -> Router:
    """Get migration router instance."""
    if database is None:
        database = get_database()
    return Router(database, migrate_dir=MIGRATIONS_DIR)


def run_migrations() -> None:
    """Run all pending migrations."""
    router = get_router()
    router.run()


def create_migration(name: str) -> str:
    """Create a new migration file."""
    router = get_router()
    return router.create(name)

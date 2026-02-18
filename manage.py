#!/usr/bin/env python3
"""
Management script for database migrations.

Usage:
    python manage.py migrate          - Run pending migrations
    python manage.py migrate create   - Create a new migration
    python manage.py migrate rollback - Rollback last migration
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.database import get_router, get_database
from app.config import MIGRATIONS_DIR


def show_help():
    """Show usage help."""
    print(__doc__)


def run_migrations():
    """Run all pending migrations."""
    router = get_router()
    router.run()
    print("Migrations completed successfully!")


def create_migration(name: str):
    """Create a new migration."""
    if not name:
        print("Error: Migration name is required")
        print("Usage: python manage.py migrate create <name>")
        return
    
    router = get_router()
    migration_name = router.create(name)
    print(f"Created migration: {migration_name}")


def rollback_migration():
    """Rollback the last migration."""
    router = get_router()
    router.rollback()
    print("Rollback completed!")


def show_status():
    """Show migration status."""
    router = get_router()
    print("\nMigration status:")
    print("-" * 50)
    for migration in router.todo:
        print(f"  ⏳ {migration}")
    for migration in router.done:
        print(f"  ✅ {migration}")
    print("-" * 50)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1]
    
    if command == "migrate":
        if len(sys.argv) < 3:
            run_migrations()
            return
        
        subcommand = sys.argv[2]
        
        if subcommand == "create":
            name = sys.argv[3] if len(sys.argv) > 3 else ""
            create_migration(name)
        elif subcommand == "rollback":
            rollback_migration()
        else:
            print(f"Unknown subcommand: {subcommand}")
            show_help()
    
    elif command == "status":
        show_status()
    
    elif command == "help" or command == "--help" or command == "-h":
        show_help()
    
    else:
        print(f"Unknown command: {command}")
        show_help()


if __name__ == "__main__":
    main()

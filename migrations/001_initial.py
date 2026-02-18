"""
Initial migration - create all tables.
"""
import datetime
from peewee import *
from playhouse.migrate import *


def migrate(migrator: SqliteMigrator, database: SqliteDatabase, fake: bool):
    """Create all database tables."""
    
    # TypeBase - Aircraft types
    migrator.sql(
        "CREATE TABLE type_base ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "name VARCHAR(255) UNIQUE NOT NULL,"
        "created_at DATETIME DEFAULT CURRENT_TIMESTAMP)"
    )
    
    # PodrazdBase - Divisions
    migrator.sql(
        "CREATE TABLE podrazd_base ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "name VARCHAR(255) UNIQUE NOT NULL,"
        "created_at DATETIME DEFAULT CURRENT_TIMESTAMP)"
    )
    
    # GroupBase - Maintenance groups
    migrator.sql(
        "CREATE TABLE group_base ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "plane_type_id INTEGER NOT NULL,"
        "name VARCHAR(255) UNIQUE NOT NULL,"
        "created_at DATETIME DEFAULT CURRENT_TIMESTAMP,"
        "FOREIGN KEY (plane_type_id) REFERENCES type_base(id))"
    )
    
    # SystemBase - Aircraft systems
    migrator.sql(
        "CREATE TABLE system_base ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "plane_type_id INTEGER NOT NULL,"
        "name VARCHAR(255) UNIQUE NOT NULL,"
        "group_id INTEGER NOT NULL,"
        "created_at DATETIME DEFAULT CURRENT_TIMESTAMP,"
        "FOREIGN KEY (plane_type_id) REFERENCES type_base(id),"
        "FOREIGN KEY (group_id) REFERENCES group_base(id))"
    )
    
    # AgregateBase - Aggregates/Units
    migrator.sql(
        "CREATE TABLE agregate_base ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "system_id INTEGER NOT NULL,"
        "count_on_plane INTEGER DEFAULT 1,"
        "name VARCHAR(255) NOT NULL,"
        "created_at DATETIME DEFAULT CURRENT_TIMESTAMP,"
        "FOREIGN KEY (system_id) REFERENCES system_base(id))"
    )
    
    # PlaneBase - Aircraft
    migrator.sql(
        "CREATE TABLE plane_base ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "plane_type_id INTEGER NOT NULL,"
        "podrazd_id INTEGER NOT NULL,"
        "zav_num VARCHAR(255) UNIQUE NOT NULL,"
        "bort_number VARCHAR(255) NOT NULL,"
        "created_at DATETIME DEFAULT CURRENT_TIMESTAMP,"
        "FOREIGN KEY (plane_type_id) REFERENCES type_base(id),"
        "FOREIGN KEY (podrazd_id) REFERENCES podrazd_base(id))"
    )
    
    # OsobBase - Features
    migrator.sql(
        "CREATE TABLE osob_base ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "plane_type_id INTEGER NOT NULL,"
        "name VARCHAR(255) UNIQUE NOT NULL,"
        "created_at DATETIME DEFAULT CURRENT_TIMESTAMP,"
        "FOREIGN KEY (plane_type_id) REFERENCES type_base(id))"
    )
    
    # OsobPlaneBase
    migrator.sql(
        "CREATE TABLE osob_plane_base ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "osob_id INTEGER NOT NULL,"
        "plane_id INTEGER NOT NULL,"
        "created_at DATETIME DEFAULT CURRENT_TIMESTAMP,"
        "FOREIGN KEY (osob_id) REFERENCES osob_base(id),"
        "FOREIGN KEY (plane_id) REFERENCES plane_base(id))"
    )
    
    # OsobSystemAddBase
    migrator.sql(
        "CREATE TABLE osob_system_add_base ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "osob_id INTEGER NOT NULL,"
        "system_id INTEGER NOT NULL,"
        "created_at DATETIME DEFAULT CURRENT_TIMESTAMP,"
        "FOREIGN KEY (osob_id) REFERENCES osob_base(id),"
        "FOREIGN KEY (system_id) REFERENCES system_base(id))"
    )
    
    # OsobSystemRemoveBase
    migrator.sql(
        "CREATE TABLE osob_system_remove_base ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "osob_id INTEGER NOT NULL,"
        "system_id INTEGER NOT NULL,"
        "created_at DATETIME DEFAULT CURRENT_TIMESTAMP,"
        "FOREIGN KEY (osob_id) REFERENCES osob_base(id),"
        "FOREIGN KEY (system_id) REFERENCES system_base(id))"
    )
    
    # OsobAgregateAddBase
    migrator.sql(
        "CREATE TABLE osob_agregate_add_base ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "osob_id INTEGER NOT NULL,"
        "agregate_id INTEGER NOT NULL,"
        "created_at DATETIME DEFAULT CURRENT_TIMESTAMP,"
        "FOREIGN KEY (osob_id) REFERENCES osob_base(id),"
        "FOREIGN KEY (agregate_id) REFERENCES agregate_base(id))"
    )
    
    # OsobAgregateRemoveBase
    migrator.sql(
        "CREATE TABLE osob_agregate_remove_base ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "osob_id INTEGER NOT NULL,"
        "agregate_id INTEGER NOT NULL,"
        "created_at DATETIME DEFAULT CURRENT_TIMESTAMP,"
        "FOREIGN KEY (osob_id) REFERENCES osob_base(id),"
        "FOREIGN KEY (agregate_id) REFERENCES agregate_base(id))"
    )
    
    # OtkazAgregateBase - Failures
    migrator.sql(
        "CREATE TABLE otkaz_agregate_base ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "agregate_id INTEGER NOT NULL,"
        "plane_id INTEGER NOT NULL,"
        "description VARCHAR(255) DEFAULT '',"
        "number VARCHAR(255) NOT NULL,"
        "removed INTEGER DEFAULT 0,"
        "created_at DATETIME DEFAULT CURRENT_TIMESTAMP,"
        "FOREIGN KEY (agregate_id) REFERENCES agregate_base(id),"
        "FOREIGN KEY (plane_id) REFERENCES plane_base(id))"
    )
    
    # Create indexes
    migrator.sql("CREATE UNIQUE INDEX idx_type_base_name ON type_base(name)")
    migrator.sql("CREATE UNIQUE INDEX idx_podrazd_base_name ON podrazd_base(name)")
    migrator.sql("CREATE UNIQUE INDEX idx_group_base_name ON group_base(name)")
    migrator.sql("CREATE UNIQUE INDEX idx_system_base_name ON system_base(name)")
    migrator.sql("CREATE UNIQUE INDEX idx_plane_base_zav_num ON plane_base(zav_num)")
    migrator.sql("CREATE UNIQUE INDEX idx_osob_base_name ON osob_base(name)")


def rollback(migrator: SqliteMigrator, database: SqliteDatabase, fake: bool):
    """Drop all tables."""
    migrator.sql("DROP TABLE IF EXISTS otkaz_agregate_base")
    migrator.sql("DROP TABLE IF EXISTS osob_agregate_remove_base")
    migrator.sql("DROP TABLE IF EXISTS osob_agregate_add_base")
    migrator.sql("DROP TABLE IF EXISTS osob_system_remove_base")
    migrator.sql("DROP TABLE IF EXISTS osob_system_add_base")
    migrator.sql("DROP TABLE IF EXISTS osob_plane_base")
    migrator.sql("DROP TABLE IF EXISTS osob_base")
    migrator.sql("DROP TABLE IF EXISTS plane_base")
    migrator.sql("DROP TABLE IF EXISTS agregate_base")
    migrator.sql("DROP TABLE IF EXISTS system_base")
    migrator.sql("DROP TABLE IF EXISTS group_base")
    migrator.sql("DROP TABLE IF EXISTS podrazd_base")
    migrator.sql("DROP TABLE IF EXISTS type_base")

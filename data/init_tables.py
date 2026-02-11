from peewee import SqliteDatabase

from data.example import example_data
from data.data import PlaneBase, SystemBase, TypeBase, OtkazAgregateBase, PodrazdBase, GroupBase, \
    AgregateBase, OsobSystemRemoveBase, OsobPlaneBase, OsobSystemAddBase, OsobTypeBase

db = SqliteDatabase('./data/database.db', pragmas={'foreign_keys': 1})

def create_tables():
    with db:
        db.create_tables(
            [
                PlaneBase, SystemBase, TypeBase,
                OtkazAgregateBase,
                PodrazdBase, GroupBase, AgregateBase,
                OsobSystemRemoveBase, OsobPlaneBase, OsobSystemAddBase, OsobTypeBase
            ]
        )

def drop_tables():
    with db:
        db.drop_tables(
            [
                PlaneBase, SystemBase, TypeBase,
                OtkazAgregateBase,
                PodrazdBase, GroupBase, AgregateBase,
                OsobSystemRemoveBase, OsobPlaneBase, OsobSystemAddBase, OsobTypeBase
            ]
        )

def fill_tables():
    example_data()

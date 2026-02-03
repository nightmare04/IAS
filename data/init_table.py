from peewee import SqliteDatabase

from data import PlaneBase, PlaneSystemBase, PlaneTypeBase, OtkazAgregateBase, SpecBase, PodrazdBase, GroupBase, \
    AgregateBase
from data.example import example_data

db = SqliteDatabase('./data/database.db', pragmas={'foreign_keys': 1})

def create_tables():
    with db:
        db.create_tables(
            [
                PlaneBase, PlaneSystemBase, PlaneTypeBase,
                OtkazAgregateBase,
                SpecBase, PodrazdBase, GroupBase, AgregateBase
            ]
        )

def drop_tables():
    with db:
        db.drop_tables(
            [
                PlaneBase, PlaneSystemBase, PlaneTypeBase,
                OtkazAgregateBase,
                SpecBase, PodrazdBase, GroupBase, AgregateBase
            ]
        )

def fill_tables():
    example_data()
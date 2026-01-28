from peewee import Model
from playhouse.sqlite_ext import SqliteExtDatabase


db = SqliteExtDatabase('./database/pw.db', pragmas={'foreign_keys': 1})
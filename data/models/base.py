"""Base model and database connection."""
import datetime

from peewee import DateTimeField, IntegerField, Model

from app.database import get_database

db = get_database()


class BaseModel(Model):
    """Base model with auto-increment ID and created_at timestamp."""
    id = IntegerField(primary_key=True)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

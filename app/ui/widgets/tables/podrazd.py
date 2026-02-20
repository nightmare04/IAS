"""Table view for divisions."""
from typing import Any

from app.ui.models.reference import PodrazdModel

from .base import UnTableView


class PodrazdTable(UnTableView):
    """Table view for divisions."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.table_model = PodrazdModel()
        self.setModel(self.table_model)

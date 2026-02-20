"""Table view for aircraft features."""
from typing import Any

from app.ui.models.reference import OsobModel

from .base import UnTableView


class OsobTable(UnTableView):
    """Table view for aircraft features."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.table_model = OsobModel()
        self.setModel(self.table_model)

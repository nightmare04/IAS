"""Table view for aircraft serviceability data."""
from typing import Any

from PyQt6.QtCore import QTimer

from app.models.aircraft import PlaneBase
from app.ui.models.ispravnost import IspravnostTableModel

from .base import UnTableView


class IspravnostTable(UnTableView):
    """Table view for aircraft serviceability data."""

    def __init__(self, plane: PlaneBase, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.table_model = IspravnostTableModel(plane)
        self.setModel(self.table_model)

    def set_span_for_groups(self) -> None:
        """Set row spans for group rows."""
        self.clear_all_span()
        if isinstance(self.table_model, IspravnostTableModel):
            for row in range(self.table_model.rowCount()):
                if self.table_model.get_row_type(row) == 'group':
                    self.setSpan(row, 0, 1, self.table_model.columnCount())

    def clear_all_span(self) -> None:
        """Clear all row spans."""
        if isinstance(self.table_model, IspravnostTableModel):
            rows = self.table_model.rowCount()
            cols = self.table_model.columnCount()
            for row in range(rows):
                for col in range(cols):
                    if self.rowSpan(row, col) > 1:
                        self.setSpan(row, col, 1, 1)

    def set_filter(self, filter_text: str) -> None:
        """Set filter for table data."""
        pass

    def load_data(self) -> None:
        """Load data from database."""
        self.table_model.load_data()
        self.clear_all_span()
        QTimer.singleShot(0, self.set_span_for_groups)

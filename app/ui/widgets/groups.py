"""Group widgets for displaying aircraft by division."""
from typing import TYPE_CHECKING, Any

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QGridLayout, QGroupBox

from app.ui.widgets.buttons import PlaneBtn

if TYPE_CHECKING:
    from app.models.aircraft import PodrazdBase


class PodrGroup(QGroupBox):
    """Group box displaying aircraft buttons for a division."""

    open_signal = pyqtSignal(object)

    def __init__(self, podr: "PodrazdBase", parent: Any | None = None) -> None:
        super().__init__(parent)
        self.podr = podr
        self.setTitle(str(podr.name))
        self.groupLayout = QGridLayout()
        self.setLayout(self.groupLayout)
        self.load_planes()

    def load_planes(self) -> None:
        """Load aircraft buttons for this division."""
        from app.models.aircraft import PlaneBase

        planes = PlaneBase.select().where(PlaneBase.podrazd == self.podr.id)
        for p, plane in enumerate(planes):
            row_p = p // 3
            col_p = p % 3
            btn = PlaneBtn(plane)
            btn.open_signal.connect(self.open_ispravnost)
            self.groupLayout.addWidget(btn, row_p, col_p)

    def open_ispravnost(self, btn: PlaneBtn) -> None:
        """Emit open signal with aircraft button."""
        self.open_signal.emit(btn)

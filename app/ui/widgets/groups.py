"""Group widgets for displaying aircraft by division."""
from typing import TYPE_CHECKING, Any

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QGridLayout, QGroupBox

from app.ui.widgets.buttons import OsobBtn, PlaneBtn
from data.models import OsobBase, OsobPlaneBase, PlaneBase, PodrazdBase, TypeBase


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

class OsobGroup(QGroupBox):
    def __init__(self, type:TypeBase = None, parent = None):
        super().__init__(parent)
        self.type = type
        self.btns = []
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)
        if type:
            self.load_osobs(type)

    def load_osobs(self, type: TypeBase):
        osobs = OsobBase.select().where(OsobBase.plane_type == type)
        for p, osob in enumerate(osobs):
            row_p = p // 3
            col_p = p % 3
            btn = OsobBtn(osob)
            self.btns.append(btn)
            self.main_layout.addWidget(btn, row_p, col_p)

    def save_osobs(self, plane: PlaneBase):
        for btn in self.btns:
            osob = OsobPlaneBase.get_or_none(OsobPlaneBase.plane == plane)
            if btn.isChecked:
                if osob is None:
                    new_osob = OsobPlaneBase()
                    new_osob.osob = self.btn.osob
                    new_osob.plane = plane
                    new_osob.save()
            else:
                osob.delete_instance()

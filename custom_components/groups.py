from PyQt6.QtWidgets import QGroupBox, QGridLayout
from PyQt6.QtCore import pyqtSignal

from custom_components.buttons import PlaneBtn
from data.data import PodrazdBase, PlaneBase



class PodrGroup(QGroupBox):
    open_signal = pyqtSignal(object)
    def __init__(self, podr:PodrazdBase, parent=None):
        super().__init__(parent)
        self.podr = podr
        self.setTitle(str(podr.name))
        self.groupLayout = QGridLayout()
        self.setLayout(self.groupLayout)
        self.load_planes()

    def load_planes(self):
        planes = PlaneBase.select().where(PlaneBase.podrazd == self.podr.id)
        for p, plane in enumerate(planes):
            row_p = p // 3
            col_p = p % 3
            btn = PlaneBtn(plane)
            btn.open_signal.connect(self.open_ispravnost)
            self.groupLayout.addWidget(btn, row_p, col_p)

    def open_ispravnost(self, btn:PlaneBtn):
        self.open_signal.emit(btn)


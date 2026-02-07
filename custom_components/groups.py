from PyQt6.QtWidgets import QGroupBox, QGridLayout

from custom_components.buttons import PlaneBtn
from data.data_models import PodrazdBase, PlaneBase


class PodrGroup(QGroupBox):
    def __init__(self, podr:PodrazdBase, parent=None):
        super().__init__(parent)
        self.podr = podr
        self.setTitle(podr.name)
        self.groupLayout = QGridLayout()
        self.setLayout(self.groupLayout)

    def load_planes(self):
        planes = PlaneBase.select().where(PlaneBase.podrazd == self.podr.id)
        for p, plane in enumerate(planes):
            row_p = p // 3
            col_p = p % 3
            btn = PlaneBtn(plane)
            self.groupLayout.addWidget(btn, row_p, col_p)

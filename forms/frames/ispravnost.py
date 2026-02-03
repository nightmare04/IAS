from PyQt6.QtWidgets import QFrame, QGridLayout, QAbstractItemView
from data.models import PodrazdBase
from forms.custom_components.buttons import PlaneBtn
from forms.custom_components.groups import PodrGroup


class IspravnostFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.load_condition()

    def load_condition(self):
        podr_data = PodrazdBase.select()
        podr_layout = QGridLayout()
        for i, podr in enumerate(podr_data):
            group = PodrGroup(podr)
            group.load_planes()
            row = i // 2
            col = i % 2
            podr_layout.addWidget(group, row, col)
        self.setLayout(podr_layout)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.deleteLater()
            else:
                sublayout = item.layout()
                if sublayout is not None:
                    self.clear_layout(sublayout)

    def update_ispravnost(self):
        for plane_bnt in self.findChildren(PlaneBtn):
            plane_bnt.update_color()
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QComboBox

from data.data_models import SpecBase, PlaneTypeBase, GroupBase


class PlaneTypeComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_data()

    def load_data(self, data=None):
        self.clear()
        list_data = PlaneTypeBase.select()

        for plane_type in list_data:
            self.addItem(plane_type.name, plane_type.id)


class SpecComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)

    def load_data(self, data=None):
        self.clear()
        if data is None:
            list_data = SpecBase.select()
        else:
            list_data = SpecBase.select().where(SpecBase.plane_type == data)

        for spec in list_data:
            self.addItem(spec.name, spec.id)


class GroupComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)

    def load_data(self, data=None):
        self.clear()
        if data is None:
            list_data = GroupBase.select()
        else:
            list_data = GroupBase.select().where(GroupBase.spec == data)

        for spec in list_data:
            self.addItem(spec.name, spec.id)

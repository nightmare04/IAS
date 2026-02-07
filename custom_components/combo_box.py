from PyQt6.QtWidgets import QComboBox

from data.data_models import PlaneTypeBase, GroupBase, PlaneSystemBase, AgregateBase


class PlaneTypeComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_data()

    def load_data(self):
        self.clear()
        self.addItem("Выберите тип самолета", 0)
        list_data = PlaneTypeBase.select()
        for plane_type in list_data:
            self.addItem(plane_type.name, plane_type.id)


class GroupComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addItem("Сначала выберете тип самолета...")

    def load_data(self, data=None):
        self.clear()
        self.addItem("Выберите группу обслуживания", 0)
        if data is None:
            list_data = GroupBase.select()
        else:
            list_data = GroupBase.select().where(GroupBase.plane_type == data)

        for spec in list_data:
            self.addItem(spec.name, spec.id)


class SystemComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addItem("Сначала выберете группу обслуживания...")

    def load_data(self, data=None):
        self.clear()
        self.addItem("Выберите систему самолета")
        if data:
            list_data = PlaneSystemBase.select().where(PlaneSystemBase.group == data)
            for system in list_data:
                self.addItem(system.name, system.id)


class AgregateComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)

    def load_data(self, data=None):
        self.clear()
        self.addItem("Выберите блок/агрегат")
        if data:
            list_data = AgregateBase.select().where(AgregateBase.system == data)
            for agregate in list_data:
                self.addItem(agregate.name, agregate.id)

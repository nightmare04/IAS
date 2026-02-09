from peewee import SqliteDatabase

from data.data import PlaneTypeBase, GroupBase, PlaneSystemBase, PodrazdBase, PlaneBase, AgregateBase, \
    OtkazAgregateBase, OsobSystemRemoveBase, OsobPlaneBase, OsobSystemAddBase, OsobBase

db = SqliteDatabase('./data/database.db', pragmas={'foreign_keys': 1})

plane_type_data = [
    {'name': 'Ту-95МС'},
    {'name': 'Ту-22М3'}
]
podrazd_data = [
    {'name': '1 АЭ'},
    {'name': '2 АЭ'},
    {'name': '3 АЭ'},
    {'name': '4 АЭ'},
]
planes_data = [
    {'bort_number': '50', 'zav_num': '6403423300822', 'plane_type': 1, 'podrazd': 3},
    {'bort_number': '51', 'zav_num': '6403423300823', 'plane_type': 1, 'podrazd': 3},
    {'bort_number': '52', 'zav_num': '6403423300824', 'plane_type': 1, 'podrazd': 3},
    {'bort_number': '53', 'zav_num': '6403423301825', 'plane_type': 1, 'podrazd': 3},
    {'bort_number': '54', 'zav_num': '6403423300826', 'plane_type': 1, 'podrazd': 3},
    {'bort_number': '55', 'zav_num': '6403423310827', 'plane_type': 1, 'podrazd': 3},
    {'bort_number': '56', 'zav_num': '6403422300828', 'plane_type': 1, 'podrazd': 3},
    {'bort_number': '57', 'zav_num': '6403423100829', 'plane_type': 1, 'podrazd': 3},
    {'bort_number': '58', 'zav_num': '6403413300820', 'plane_type': 1, 'podrazd': 3},
    {'bort_number': '60', 'zav_num': '6403423300812', 'plane_type': 1, 'podrazd': 1},
    {'bort_number': '61', 'zav_num': '6403423301823', 'plane_type': 1, 'podrazd': 1},
    {'bort_number': '62', 'zav_num': '6403422300824', 'plane_type': 1, 'podrazd': 1},
    {'bort_number': '63', 'zav_num': '6403423300825', 'plane_type': 1, 'podrazd': 1},
    {'bort_number': '64', 'zav_num': '6403423301826', 'plane_type': 1, 'podrazd': 1},
    {'bort_number': '65', 'zav_num': '6403423300827', 'plane_type': 1, 'podrazd': 1},
    {'bort_number': '66', 'zav_num': '6403423300828', 'plane_type': 1, 'podrazd': 1},
    {'bort_number': '67', 'zav_num': '6403423300829', 'plane_type': 1, 'podrazd': 1},
    {'bort_number': '68', 'zav_num': '6403423300820', 'plane_type': 1, 'podrazd': 1},
]
plane_system_data = [
    {'plane_type': 1, 'name': 'Система СКВ', 'group': 1},
    {'plane_type': 1, 'name': 'Система запуска', 'group': 1},
    {'plane_type': 1, 'name': 'Система запуска ВСУ', 'group': 1},
    {'plane_type': 1, 'name': 'Приборы контроля работы двигателя', 'group': 3},
    {'plane_type': 1, 'name': 'РУМБ-1Б', 'group': 2},
]
agregate_data = [
    {'plane_type': 1, 'system': 1,  'name': '2714А 2с.'},
    {'plane_type': 1, 'system': 1,  'name': 'заслонка 1932Т'},
    {'plane_type': 1, 'system': 1,  'name': 'заслонка 1919Т'},
    {'plane_type': 1, 'system': 2,  'name': 'ПР-12'},
    {'plane_type': 1, 'system': 2,  'name': 'АПД-30ТА'},
    {'plane_type': 1, 'system': 4,  'name': 'МТ-50'},
    {'plane_type': 1, 'system': 4,  'name': 'ДТ-5М'},
    {'plane_type': 1, 'system': 3,  'name': 'ЭРРД-12'},
    {'plane_type': 1, 'system': 5,  'name': 'БУГ-14'},
    {'plane_type': 1, 'system': 5,  'name': 'БК-12'},
]


group_data = [
    {'plane_type': 1, 'spec':3, 'name': 'ЭО и ЭА'},
    {'plane_type': 1, 'spec': 3, 'name': 'ПНК'},
    {'plane_type': 1, 'spec': 3, 'name': 'ПК и ФО'},
]

otkaz_agr_data = [
    {'plane': 1, 'number': '321123', 'agregate': 1},
    {'plane': 1, 'number': '321123', 'agregate': 8},
    {'plane': 1, 'number': '321123', 'agregate': 6},
    {'plane': 1, 'number': '321123', 'agregate': 9},
    {'plane': 1, 'number': '321123', 'agregate': 10},
]

osobs_data = [
    {'plane_type': 1, 'name': 'M1'},
    {'plane_type': 1, 'name': 'M2'},
]

osob_plane_data = [
    {'plane': 1, 'osob': '1'},
    {'plane': 1, 'osob': '2'},
]

system_add_data = [
    {'osob': 1, 'system': 5},
    {'osob': 2, 'system': 4},
]

system_remove_data = [
    {'osob': 1, 'system': 3},
    {'osob': 2, 'system': 2},
]

def example_data():
    with db.atomic():
        for types in plane_type_data:
            PlaneTypeBase.create(**types)
        for group in group_data:
            GroupBase.create(**group)
        for system in plane_system_data:
            PlaneSystemBase.create(**system)
        for podr in podrazd_data:
            PodrazdBase.create(**podr)
        for plane in planes_data:
            PlaneBase.create(**plane)
        for agregate in agregate_data:
            AgregateBase.create(**agregate)
        for otkaz in otkaz_agr_data:
            OtkazAgregateBase.create(**otkaz)
        for data in osobs_data:
            OsobBase.create(**data)
        for data in osob_plane_data:
            OsobPlaneBase.create(**data)
        for data in system_add_data:
            OsobSystemAddBase.create(**data)
        for data in system_remove_data:
            OsobSystemRemoveBase.create(**data)


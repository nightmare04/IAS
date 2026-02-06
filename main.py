import sys
from PyQt6.QtWidgets import QApplication

from data import init_tables
from forms.main_form import MainForm


def init_app():
    init_tables.drop_tables()
    init_tables.create_tables()
    init_tables.fill_tables()


def main():
    """Точка входа в приложение"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    init_app()
    main_form = MainForm()
    main_form.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

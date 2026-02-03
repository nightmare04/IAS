import sys
from PyQt6.QtWidgets import QApplication

from data import init_table
from forms import MainForm


def init_app():
    init_table.drop_tables()
    init_table.create_tables()
    init_table.fill_tables()


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

import sys
from PyQt6.QtWidgets import QApplication
from forms import MainForm


def main():
    """Точка входа в приложение"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    main_form = MainForm()
    main_form.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()

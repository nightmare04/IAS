import sys
from datetime import datetime
from peewee import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtGui import QAction
# Создаем базу данных Peewee
database = SqliteDatabase('example.db')


# Определяем модели Peewee
class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    name = CharField()
    email = CharField(unique=True)
    age = IntegerField()
    created_at = DateTimeField(default=datetime.now)
    is_active = BooleanField(default=True)


class Product(BaseModel):
    name = CharField()
    price = DecimalField(max_digits=10, decimal_places=2)
    quantity = IntegerField()
    category = CharField()


# Создаем таблицы
database.create_tables([User, Product])


class PeeweeTableModel(QAbstractTableModel):
    """Модель таблицы на основе Peewee"""

    def __init__(self, peewee_model, columns=None, parent=None):
        super().__init__(parent)
        self.peewee_model = peewee_model
        self.columns = columns or self._get_default_columns()
        self.refresh_data()

    def _get_default_columns(self):
        """Получаем колонки из модели Peewee"""
        columns = []
        for field_name, field in self.peewee_model._meta.fields.items():
            columns.append({
                'name': field_name,
                'title': field_name.replace('_', ' ').title(),
                'type': type(field)
            })
        return columns

    def refresh_data(self):
        """Обновляем данные из базы"""
        self.beginResetModel()
        self.data = list(self.peewee_model.select().dicts())
        self.endResetModel()

    def rowCount(self, parent=None):
        return len(self.data)

    def columnCount(self, parent=None):
        return len(self.columns)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            column_name = self.columns[index.column()]['name']
            value = self.data[index.row()][column_name]

            # Форматирование специальных типов
            if isinstance(value, datetime):
                return value.strftime('%Y-%m-%d %H:%M:%S')
            return str(value)

        elif role == Qt.ItemDataRole.TextAlignmentRole:
            # Выравнивание для числовых полей
            column_type = self.columns[index.column()]['type']
            if column_type in [IntegerField, DecimalField, FloatField]:
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.columns[section]['title']
            elif orientation == Qt.Orientation.Vertical:
                return str(section + 1)
        return None


class UserManagementWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

        # Заполняем тестовыми данными
        self.create_sample_data()

    def init_ui(self):
        self.setWindowTitle('Управление пользователями на Peewee')
        self.setGeometry(100, 100, 900, 600)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Панель инструментов
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Кнопки
        btn_add = QAction('Добавить', self)
        btn_add.triggered.connect(self.add_user)
        toolbar.addAction(btn_add)

        btn_edit = QAction('Редактировать', self)
        btn_edit.triggered.connect(self.edit_user)
        toolbar.addAction(btn_edit)

        btn_delete = QAction('Удалить', self)
        btn_delete.triggered.connect(self.delete_user)
        toolbar.addAction(btn_delete)

        btn_refresh = QAction('Обновить', self)
        btn_refresh.triggered.connect(self.refresh_table)
        toolbar.addAction(btn_refresh)

        # Таблица пользователей
        self.table_view = QTableView()
        self.table_model = PeeweeTableModel(User)
        self.table_view.setModel(self.table_model)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        # Настройка ширины колонок
        self.table_view.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(self.table_view)

        # Статус бар
        self.statusBar().showMessage('Готово')

    def create_sample_data(self):
        """Создание тестовых данных"""
        if not User.select().exists():
            users = [
                {'name': 'Иван Иванов', 'email': 'ivan@example.com', 'age': 25, 'is_active': True},
                {'name': 'Мария Петрова', 'email': 'maria@example.com', 'age': 30, 'is_active': True},
                {'name': 'Алексей Сидоров', 'email': 'alex@example.com', 'age': 35, 'is_active': False},
            ]
            User.insert_many(users).execute()
            self.refresh_table()

    def add_user(self):
        """Добавление нового пользователя"""
        dialog = UserDialog(self)
        if dialog.exec():
            try:
                data = dialog.get_data()
                User.create(**data)
                self.refresh_table()
                self.statusBar().showMessage('Пользователь добавлен')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось добавить пользователя: {str(e)}')

    def edit_user(self):
        """Редактирование выбранного пользователя"""
        selected = self.table_view.selectionModel().selectedRows()
        if not selected:
            QMessageBox.warning(self, 'Внимание', 'Выберите пользователя для редактирования')
            return

        index = selected[0]
        user_id = self.table_model.data[index.row()]['id']
        user = User.get_by_id(user_id)

        dialog = UserDialog(self, user)
        if dialog.exec():
            try:
                data = dialog.get_data()
                User.update(**data).where(User.id == user_id).execute()
                self.refresh_table()
                self.statusBar().showMessage('Пользователь обновлен')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось обновить пользователя: {str(e)}')

    def delete_user(self):
        """Удаление выбранного пользователя"""
        selected = self.table_view.selectionModel().selectedRows()
        if not selected:
            QMessageBox.warning(self, 'Внимание', 'Выберите пользователя для удаления')
            return

        reply = QMessageBox.question(
            self, 'Подтверждение',
            'Вы уверены, что хотите удалить выбранного пользователя?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            index = selected[0]
            user_id = self.table_model.data[index.row()]['id']
            User.delete_by_id(user_id)
            self.refresh_table()
            self.statusBar().showMessage('Пользователь удален')

    def refresh_table(self):
        """Обновление таблицы"""
        self.table_model.refresh_data()
        self.table_view.viewport().update()


class UserDialog(QDialog):
    """Диалог для добавления/редактирования пользователя"""

    def __init__(self, parent=None, user=None):
        super().__init__(parent)
        self.user = user
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Добавить пользователя' if not self.user else 'Редактировать пользователя')
        self.setModal(True)

        layout = QFormLayout(self)

        # Поля ввода
        self.name_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.age_spinbox = QSpinBox()
        self.age_spinbox.setRange(1, 120)
        self.active_checkbox = QCheckBox('Активен')

        # Если редактируем существующего пользователя
        if self.user:
            self.name_edit.setText(self.user.name)
            self.email_edit.setText(self.user.email)
            self.age_spinbox.setValue(self.user.age)
            self.active_checkbox.setChecked(self.user.is_active)

        layout.addRow('Имя:', self.name_edit)
        layout.addRow('Email:', self.email_edit)
        layout.addRow('Возраст:', self.age_spinbox)
        layout.addRow(self.active_checkbox)

        # Кнопки
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_data(self):
        """Получение данных из формы"""
        return {
            'name': self.name_edit.text(),
            'email': self.email_edit.text(),
            'age': self.age_spinbox.value(),
            'is_active': self.active_checkbox.isChecked()
        }


def main():
    app = QApplication(sys.argv)

    # Устанавливаем стиль
    app.setStyle('Fusion')

    window = UserManagementWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QListWidgetItem,
                             QMessageBox, QInputDialog)
#from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi


class TaskPlanner(QMainWindow):
    def __init__(self):
        super().__init__()

        # Загружаем UI из файла
        loadUi('NewUIFile.ui', self)

        # Наполняем списки тестовыми задачами
        self.initialize_tasks()

        # Настройка начального состояния кнопок
        self.update_buttons_state()

        # Подключение сигналов
        self.pushButton_Add.clicked.connect(self.add_task)
        self.pushButton_Delete.clicked.connect(self.delete_task)
        self.pushButton_Left.clicked.connect(self.move_left)
        self.pushButton_Right.clicked.connect(self.move_right)

        # Отслеживаем активный список (в котором было последнее выделение)
        self.active_list = None
        self.listWidgetCurrentTasks.itemSelectionChanged.connect(self.set_active_current)
        self.listWidgetCompletedTasks.itemSelectionChanged.connect(self.set_active_completed)

        # Первоначальное обновление
        self.update_all_tasks_list()

    def initialize_tasks(self):
        """Инициализация списков тестовыми задачами"""
        current_tasks = [
            "Рефакторинг legacy-кода",
            "Написание unit-тестов для модуля API",
            "Оптимизация SQL-запросов",
            "Интеграция с новым платежным шлюзом",
            "Разработка асинхронного веб-скрапера",
            "Обновление зависимостей в requirements.txt",
            "Создание документации для нового API",
            "Реализация кэширования для тяжелых запросов",
            "Настройка CI/CD pipeline",
            "Оптимизация загрузки Docker-образов",
            "Разработка Telegram-бота для мониторинга",
            "Миграция на Python 3.11"
        ]

        completed_tasks = [
            "Фикс бага с кодировкой в CSV-экспорте",
            "Реализация JWT-аутентификации",
            "Настройка логгирования приложения",
            "Создание базового Dockerfile",
            "Интеграция Sentry для ошибок",
            "Написание скрипта для бэкапа БД",
            "Реализация REST API для пользователей",
            "Настройка pre-commit hooks",
            "Деплой на staging-сервер",
            "Оптимизация загрузки статики",
            "Реализация пагинации в API",
            "Написание конфига для Nginx",
            "Автоматизация тестового наполнения БД"
        ]

        for task in current_tasks:
            self.listWidgetCurrentTasks.addItem(QListWidgetItem(task))

        for task in completed_tasks:
            self.listWidgetCompletedTasks.addItem(QListWidgetItem(task))

    def set_active_current(self):
        """Устанавливаем текущие задачи как активный список"""
        self.active_list = self.listWidgetCurrentTasks
        self.update_buttons_state()

    def set_active_completed(self):
        """Устанавливаем завершенные задачи как активный список"""
        self.active_list = self.listWidgetCompletedTasks
        self.update_buttons_state()

    def add_task(self):
        """Добавление новой задачи в текущие"""
        task_text, ok = QInputDialog.getText(self, 'Добавить задачу', 'Введите описание задачи:')
        if ok and task_text:
            item = QListWidgetItem(task_text)
            self.listWidgetCurrentTasks.addItem(item)
            self.update_all_tasks_list()
            self.active_list = self.listWidgetCurrentTasks

    def delete_task(self):
        """Удаление задачи из активного списка"""
        if not self.active_list or not self.active_list.selectedItems():
            QMessageBox.information(self, 'Информация', 'Выберите задачу для удаления')
            return

        # Получаем выбранные элементы и удаляем их
        selected_items = self.active_list.selectedItems()
        for item in selected_items:
            self.active_list.takeItem(self.active_list.row(item))

        self.update_all_tasks_list()

    def move_right(self):
        """Перемещение из текущих в выполненные"""
        if not self.listWidgetCurrentTasks.selectedItems():
            return

        selected = self.listWidgetCurrentTasks.selectedItems()
        for item in selected:
            new_item = QListWidgetItem(item.text())
            self.listWidgetCompletedTasks.addItem(new_item)
            self.listWidgetCurrentTasks.takeItem(self.listWidgetCurrentTasks.row(item))

        self.update_all_tasks_list()
        self.active_list = self.listWidgetCompletedTasks

    def move_left(self):
        """Перемещение из выполненных в текущие"""
        if not self.listWidgetCompletedTasks.selectedItems():
            return

        selected = self.listWidgetCompletedTasks.selectedItems()
        for item in selected:
            new_item = QListWidgetItem(item.text())
            self.listWidgetCurrentTasks.addItem(new_item)
            self.listWidgetCompletedTasks.takeItem(self.listWidgetCompletedTasks.row(item))

        self.update_all_tasks_list()
        self.active_list = self.listWidgetCurrentTasks

    def update_buttons_state(self):
        """Обновление состояния кнопок"""
        current_selected = bool(self.listWidgetCurrentTasks.selectedItems())
        completed_selected = bool(self.listWidgetCompletedTasks.selectedItems())

        self.pushButton_Right.setEnabled(current_selected)
        self.pushButton_Left.setEnabled(completed_selected)
        self.pushButton_Delete.setEnabled(current_selected or completed_selected)

    def update_all_tasks_list(self):
        """Обновление списка всех задач"""
        self.listWidgetAllTasks.clear()

        # Добавляем текущие задачи
        for i in range(self.listWidgetCurrentTasks.count()):
            self.listWidgetAllTasks.addItem(self.listWidgetCurrentTasks.item(i).text())

        # Добавляем выполненные задачи
        for i in range(self.listWidgetCompletedTasks.count()):
            self.listWidgetAllTasks.addItem(self.listWidgetCompletedTasks.item(i).text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = TaskPlanner()
    window.show()
    sys.exit(app.exec_())
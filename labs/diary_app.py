#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Приложение-ежедневник.

Модуль предоставляет CRUD-операции для управления задачами:
- Добавление, редактирование, удаление задач
- Отметка выполнения
- Фильтрация по дате
- Поиск по описанию
- Экспорт в текстовый файл

Данные сохраняются в JSON файл.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

from typing_extensions import TypedDict

# Константы для путей
DEFAULT_DATA_FILENAME: str = "tasks.json"
DATA_DIRECTORY: str = "data"
DEFAULT_EXPORT_FILENAME: str = "tasks_export.txt"

# Константы для форматов
DATE_FORMAT: str = "%d.%m.%Y"
TIME_FORMAT: str = "%H:%M"

# Символы статуса
STATUS_COMPLETED: str = "✓"
STATUS_PENDING: str = "✗"

# Сообщения об ошибках
ERROR_EMPTY_DESCRIPTION: str = "Описание не может быть пустым!"
ERROR_INVALID_DATE: str = "Неверный формат даты! Используется сегодняшняя."
ERROR_INVALID_ID: str = "Неверный ID. Ожидается число."
ERROR_TASK_NOT_FOUND: str = "Задача с таким ID не найдена."
ERROR_FILE_CORRUPTED: str = "Файл с задачами повреждён. Начинаем с пустого списка."
ERROR_EXPORT_FAILED: str = "Не удалось экспортировать файл: {error}"
ERROR_EMPTY_QUERY: str = "Запрос пуст."
ERROR_NO_TASKS: str = "Нет задач."
ERROR_NOTHING_FOUND: str = "Ничего не найдено."

# Заголовки меню
MENU_TITLE: str = "=== Ежедневник ==="
MENU_ADD_TASK: str = "--- Добавление задачи ---"
MENU_TASK_LIST: str = "--- Список задач ---"


class TaskData(TypedDict):
    """Структура данных о задаче."""
    id: int
    description: str
    date: str
    time: Optional[str]
    completed: bool


class DiaryApp:
    """
    Приложение для управления задачами (ежедневник).

    Предоставляет CRUD-операции для задач, фильтрацию,
    поиск и экспорт данных.
    """

    def __init__(self, data_file: Optional[Path] = None) -> None:
        """
        Инициализация приложения.

        Args:
            data_file: Путь к файлу данных (опционально).
        """
        self._tasks: List[TaskData] = []
        self._next_id: int = 1
        self._data_file = data_file or self._get_default_data_file()

    def _get_default_data_file(self) -> Path:
        """Получение пути к файлу данных по умолчанию."""
        project_root = Path(__file__).resolve().parent.parent
        data_dir = project_root / DATA_DIRECTORY
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir / DEFAULT_DATA_FILENAME

    def load_tasks(self) -> bool:
        """
        Загрузка задач из JSON файла.

        Returns:
            True, если загрузка успешна, False в случае ошибки.
        """
        try:
            with open(self._data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._tasks = [TaskData(**task) for task in data]
                # Обновляем next_id на основе максимального ID
                if self._tasks:
                    self._next_id = max(task['id'] for task in self._tasks) + 1
            return True
        except FileNotFoundError:
            return True  # Пустой список - это нормально
        except (json.JSONDecodeError, KeyError, TypeError):
            print(ERROR_FILE_CORRUPTED)
            self._tasks = []
            return False

    def save_tasks(self) -> bool:
        """
        Сохранение задач в JSON файл.

        Returns:
            True, если сохранение успешно, False в случае ошибки.
        """
        try:
            with open(self._data_file, "w", encoding="utf-8") as f:
                json.dump(self._tasks, f, ensure_ascii=False, indent=4)
            return True
        except IOError as e:
            print(f"Ошибка сохранения: {e}")
            return False

    def add_task(
        self,
        description: str,
        date: Optional[datetime] = None,
        time: Optional[str] = None
    ) -> Optional[TaskData]:
        """
        Добавление новой задачи.

        Args:
            description: Описание задачи.
            date: Дата задачи (по умолчанию сегодня).
            time: Время задачи (опционально).

        Returns:
            Добавленную задачу или None, если описание пустое.
        """
        if not description:
            print(ERROR_EMPTY_DESCRIPTION)
            return None

        if date is None:
            date = datetime.now()

        task = TaskData(
            id=self._next_id,
            description=description,
            date=date.strftime(DATE_FORMAT),
            time=time,
            completed=False,
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_task_by_id(self, task_id: int) -> Optional[TaskData]:
        """
        Поиск задачи по ID.

        Args:
            task_id: ID задачи.

        Returns:
            Задача или None, если не найдена.
        """
        for task in self._tasks:
            if task['id'] == task_id:
                return task
        return None

    def mark_completed(self, task_id: int) -> bool:
        """
        Отметка задачи как выполненной.

        Args:
            task_id: ID задачи.

        Returns:
            True, если задача найдена и отмечена, False иначе.
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            print(ERROR_TASK_NOT_FOUND)
            return False

        task['completed'] = True
        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Удаление задачи.

        Args:
            task_id: ID задачи.

        Returns:
            True, если задача найдена и удалена, False иначе.
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            print(ERROR_TASK_NOT_FOUND)
            return False

        self._tasks.remove(task)
        return True

    def edit_task(
        self,
        task_id: int,
        description: Optional[str] = None,
        date: Optional[datetime] = None,
        time: Optional[str] = None
    ) -> bool:
        """
        Редактирование задачи.

        Args:
            task_id: ID задачи.
            description: Новое описание (опционально).
            date: Новая дата (опционально).
            time: Новое время (опционально).

        Returns:
            True, если задача найдена и обновлена, False иначе.
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            print(ERROR_TASK_NOT_FOUND)
            return False

        if description:
            task['description'] = description
        if date:
            task['date'] = date.strftime(DATE_FORMAT)
        if time is not None:
            task['time'] = time

        return True

    def get_sorted_tasks(self) -> List[TaskData]:
        """
        Получение отсортированного списка задач.

        Returns:
            Список задач, отсортированный по дате и времени.
        """
        return sorted(
            self._tasks,
            key=lambda t: (
                datetime.strptime(t["date"], DATE_FORMAT),
                t["time"] or "00:00",
            ),
        )

    def get_tasks_by_date(self, target_date: datetime) -> List[TaskData]:
        """
        Получение задач на конкретную дату.

        Args:
            target_date: Целевая дата.

        Returns:
            Список задач на указанную дату.
        """
        return [
            task for task in self.get_sorted_tasks()
            if datetime.strptime(task["date"], DATE_FORMAT).date() == target_date.date()
        ]

    def search_by_description(self, query: str) -> List[TaskData]:
        """
        Поиск задач по описанию.

        Args:
            query: Поисковый запрос.

        Returns:
            Список найденных задач.
        """
        query_lower = query.lower()
        return [
            task for task in self._tasks
            if query_lower in task["description"].lower()
        ]

    def export_to_text(self, filename: str = DEFAULT_EXPORT_FILENAME) -> bool:
        """
        Экспорт задач в текстовый файл.

        Args:
            filename: Имя файла для экспорта.

        Returns:
            True, если экспорт успешен, False в случае ошибки.
        """
        try:
            with open(filename, "w", encoding="utf-8") as f:
                for task in self.get_sorted_tasks():
                    status = STATUS_COMPLETED if task["completed"] else STATUS_PENDING
                    time_str = f" {task['time']}" if task["time"] else ""
                    f.write(
                        f"[{status}] {task['id']}. {task['date']}{time_str} - "
                        f"{task['description']}\n"
                    )
            return True
        except IOError as e:
            print(ERROR_EXPORT_FAILED.format(error=e))
            return False


def parse_date(date_str: str) -> datetime:
    """
    Парсинг строки даты.

    Args:
        date_str: Строка даты в формате ДД.ММ.ГГГГ.

    Returns:
        Объект datetime.

    Raises:
        ValueError: Если формат даты неверен.
    """
    return datetime.strptime(date_str, DATE_FORMAT)


def get_date_input(prompt: str) -> Optional[datetime]:
    """
    Запрос даты у пользователя.

    Args:
        prompt: Текст приглашения.

    Returns:
        Введённая дата или None, если используется дата по умолчанию.
    """
    date_str = input(prompt).strip()
    if not date_str:
        return None

    try:
        return parse_date(date_str)
    except ValueError:
        print(ERROR_INVALID_DATE)
        return None


def get_time_input(prompt: str) -> Optional[str]:
    """
    Запрос времени у пользователя.

    Args:
        prompt: Текст приглашения.

    Returns:
        Введённое время или None.
    """
    time_str = input(prompt).strip()
    return time_str if time_str else None


def get_int_input(prompt: str) -> Optional[int]:
    """
    Безопасный ввод целого числа.

    Args:
        prompt: Текст приглашения.

    Returns:
        Введённое число или None, если ввод некорректен.
    """
    try:
        return int(input(prompt).strip())
    except ValueError:
        print(ERROR_INVALID_ID)
        return None
    except KeyboardInterrupt:
        print("\nВвод прерван пользователем.")
        return None


def format_task_line(task: TaskData) -> str:
    """
    Форматирование строки задачи для вывода.

    Args:
        task: Данные задачи.

    Returns:
        Отформатированная строка.
    """
    status = STATUS_COMPLETED if task["completed"] else STATUS_PENDING
    time_str = f" {task['time']}" if task["time"] else ""
    return f"[{status}] {task['id']}. {task['date']}{time_str} - {task['description']}"


def print_tasks(tasks: List[TaskData], filter_date: Optional[datetime] = None) -> None:
    """
    Вывод списка задач.

    Args:
        tasks: Список задач.
        filter_date: Дата для фильтрации (опционально).
    """
    if not tasks:
        print(ERROR_NO_TASKS)
        return

    sorted_tasks = sorted(
        tasks,
        key=lambda t: (
            datetime.strptime(t["date"], DATE_FORMAT),
            t["time"] or "00:00",
        ),
    )

    print(f"\n{MENU_TASK_LIST}")
    for task in sorted_tasks:
        task_date = datetime.strptime(task["date"], DATE_FORMAT).date()
        if filter_date and task_date != filter_date.date():
            continue
        print(format_task_line(task))


def print_menu() -> None:
    """Вывод главного меню."""
    print(f"\n{MENU_TITLE}")
    print("1. Показать все задачи")
    print("2. Показать задачи на сегодня")
    print("3. Показать задачи на завтра")
    print("4. Добавить задачу")
    print("5. Отметить выполненной")
    print("6. Удалить задачу")
    print("7. Редактировать задачу")
    print("8. Поиск по описанию")
    print("9. Экспортировать задачи в текст")
    print("0. Выход")


def main() -> None:
    """
    Основная функция программы.

    Запускает интерактивный цикл управления задачами.
    """
    app = DiaryApp()
    app.load_tasks()

    while True:
        print_menu()

        try:
            choice = input("Выберите действие: ").strip()
        except KeyboardInterrupt:
            print("\nРабота программы прервана.")
            app.save_tasks()
            break

        if choice == "1":
            print_tasks(app.get_sorted_tasks())

        elif choice == "2":
            print_tasks(app.get_sorted_tasks(), datetime.now())

        elif choice == "3":
            tomorrow = datetime.now() + timedelta(days=1)
            print_tasks(app.get_sorted_tasks(), tomorrow)

        elif choice == "4":
            print(f"\n{MENU_ADD_TASK}")
            description = input("Описание задачи: ").strip()
            date = get_date_input("Дата (ДД.ММ.ГГГГ) или оставьте пустым для сегодня: ")
            time = get_time_input("Время (ЧЧ:ММ) или оставьте пустым: ")
            app.add_task(description, date, time)
            print("Задача добавлена!")

        elif choice == "5":
            task_id = get_int_input("Введите ID задачи для отметки: ")
            if task_id is not None:
                if app.mark_completed(task_id):
                    print("Задача отмечена выполненной.")

        elif choice == "6":
            task_id = get_int_input("Введите ID задачи для удаления: ")
            if task_id is not None:
                if app.delete_task(task_id):
                    print("Задача удалена.")

        elif choice == "7":
            task_id = get_int_input("Введите ID задачи для редактирования: ")
            if task_id is not None:
                task = app.get_task_by_id(task_id)
                if task:
                    print(f"Текущая задача: {task}")
                    new_desc = input("Новое описание (оставьте пустым): ").strip()
                    new_date = get_date_input("Новая дата (ДД.ММ.ГГГГ) (оставьте пустым): ")
                    new_time = get_time_input("Новое время (ЧЧ:ММ) (оставьте пустым): ")
                    app.edit_task(task_id, new_desc or None, new_date, new_time)
                    print("Задача обновлена.")

        elif choice == "8":
            query = input("Введите ключевое слово для поиска в описании: ").strip()
            if query:
                found = app.search_by_description(query)
                if found:
                    print_tasks(found)
                else:
                    print(ERROR_NOTHING_FOUND)
            else:
                print(ERROR_EMPTY_QUERY)

        elif choice == "9":
            if app.export_to_text():
                print(f"Задачи экспортированы в файл '{DEFAULT_EXPORT_FILENAME}'.")

        elif choice == "0":
            app.save_tasks()
            print("До свидания!")
            break

        else:
            print("Неверный ввод, попробуйте снова.")


if __name__ == "__main__":
    main()

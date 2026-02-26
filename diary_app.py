# diary_app.py

import json
from datetime import datetime, timedelta
import os

DATA_FILE = "tasks.json"

# ------------------------------
# Работа с задачами (JSON)
# ------------------------------
def load_tasks():
    """Загружает список задач из JSON. При ошибке возвращает []"""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Файл с задачами повреждён. Начинаем с пустого списка.")
        return []

def save_tasks(tasks):
    """Сохраняет задачи в JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

# ------------------------------
# CRUD‑операции
# ------------------------------
def add_task(tasks):
    print("\n--- Добавление задачи ---")
    description = input("Описание задачи: ").strip()
    if not description:
        print("Описание не может быть пустым!")
        return

    date_str = input("Дата (ДД.ММ.ГГГГ) или оставьте пустым для сегодня: ").strip()
    if not date_str:
        date = datetime.now().date()
    else:
        try:
            date = datetime.strptime(date_str, "%d.%m.%Y").date()
        except ValueError:
            print("Неверный формат даты! Используется сегодняшняя.")
            date = datetime.now().date()

    time_str = input("Время (ЧЧ:ММ) или оставьте пустым: ").strip()
    time = time_str if time_str else None

    task = {
        "id": len(tasks) + 1,
        "description": description,
        "date": date.strftime("%d.%m.%Y"),
        "time": time,
        "completed": False,
    }
    tasks.append(task)
    print("Задача добавлена!")

def show_tasks(tasks, filter_date=None):
    if not tasks:
        print("Нет задач.")
        return

    sorted_tasks = sorted(
        tasks,
        key=lambda t: (
            datetime.strptime(t["date"], "%d.%m.%Y"),
            t["time"] or "00:00",
        ),
    )
    print("\n--- Список задач ---")
    for task in sorted_tasks:
        task_date = datetime.strptime(task["date"], "%d.%m.%Y").date()
        if filter_date and task_date != filter_date:
            continue

        status = "✓" if task["completed"] else "✗"
        time_str = f" {task['time']}" if task["time"] else ""
        print(f"[{status}] {task['id']}. {task['date']}{time_str} - {task['description']}")

def mark_completed(tasks):
    try:
        task_id = int(input("Введите ID задачи для отметки: "))
    except ValueError:
        print("Неверный ID. Ожидается число.")
        return

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            print("Задача отмечена выполненной.")
            return
    print("Задача с таким ID не найдена.")

def delete_task(tasks):
    try:
        task_id = int(input("Введите ID задачи для удаления: "))
    except ValueError:
        print("Неверный ID. Ожидается число.")
        return

    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            del tasks[i]
            print("Задача удалена.")
            # Перенумеруем id
            for idx, t in enumerate(tasks, start=1):
                t["id"] = idx
            return
    print("Задача с таким ID не найдена.")

def edit_task(tasks):
    """Редактирование задачи (описание, дата, время)."""
    try:
        task_id = int(input("Введите ID задачи для редактирования: "))
    except ValueError:
        print("Неверный ID. Ожидается число.")
        return

    for task in tasks:
        if task["id"] == task_id:
            print(f"Текущая задача: {task}")
            new_desc = input("Новое описание (оставьте пустым): ").strip()
            if new_desc:
                task["description"] = new_desc

            new_date_str = input("Новая дата (ДД.ММ.ГГГГ) (оставьте пустым): ").strip()
            if new_date_str:
                try:
                    new_date = datetime.strptime(new_date_str, "%d.%m.%Y").date()
                    task["date"] = new_date.strftime("%d.%m.%Y")
                except ValueError:
                    print("Неверный формат даты. Оставлено прежнее.")

            new_time_str = input("Новое время (ЧЧ:ММ) (оставьте пустым): ").strip()
            if new_time_str:
                task["time"] = new_time_str

            print("Задача обновлена.")
            return
    print("Задача с таким ID не найдена.")

def search_tasks_by_description(tasks, query):
    """Поиск задач по частичному совпадению в описании."""
    query = query.lower()
    found = [t for t in tasks if query in t["description"].lower()]
    if not found:
        print("Ничего не найдено.")
    else:
        show_tasks(found)

def export_tasks_to_text(tasks, filename="tasks_export.txt"):
    """Экспортирует все задачи в простой текстовый файл."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for task in tasks:
                status = "✓" if task["completed"] else "✗"
                time_str = f" {task['time']}" if task["time"] else ""
                f.write(f"[{status}] {task['id']}. {task['date']}{time_str} - {task['description']}\n")
        print(f"Задачи экспортированы в файл '{filename}'.")
    except IOError as e:
        print(f"Не удалось экспортировать файл: {e}")

# ------------------------------
# Главная функция
# ------------------------------
def main():
    tasks = load_tasks()
    while True:
        print("\n=== Ежедневник ===")
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

        choice = input("Выберите действие: ").strip()
        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            show_tasks(tasks, datetime.now().date())
        elif choice == "3":
            tomorrow = datetime.now().date() + timedelta(days=1)
            show_tasks(tasks, tomorrow)
        elif choice == "4":
            add_task(tasks)
        elif choice == "5":
            mark_completed(tasks)
        elif choice == "6":
            delete_task(tasks)
        elif choice == "7":
            edit_task(tasks)
        elif choice == "8":
            query = input("Введите ключевое слово для поиска в описании: ").strip()
            if query:
                search_tasks_by_description(tasks, query)
            else:
                print("Запрос пуст.")
        elif choice == "9":
            export_tasks_to_text(tasks)
        elif choice == "0":
            save_tasks(tasks)
            print("До свидания!")
            break
        else:
            print("Неверный ввод, попробуйте снова.")

if __name__ == "__main__":
    main()

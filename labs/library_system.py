#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Библиотечная система.

Модуль предоставляет класс LibrarySystem для управления книгами,
читателями, выдачей и возвратом книг, а также учётом просрочек.
Данные сохраняются в JSON файл.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# Константы для путей
DEFAULT_DATA_FILENAME: str = "library_data.json"
DATA_DIRECTORY: str = "data"

# Константы для бизнес-логики
LOAN_PERIOD_DAYS: int = 14  # Период займа книг в днях
FINE_PER_DAY: float = 0.5  # Штраф за просрочку в день
DATE_FORMAT: str = "%Y-%m-%d"
DISPLAY_DATE_FORMAT: str = "%d.%m.%Y"

# Сообщения об ошибках
ERROR_READER_NOT_FOUND: str = "Читатель не найден!"
ERROR_BOOK_NOT_FOUND: str = "Книга не найдена!"
ERROR_BOOK_ALREADY_BORROWED: str = "Книга уже выдана!"
ERROR_BOOK_NOT_BORROWED_BY_READER: str = "Эта книга не была выдана данному читателю!"
ERROR_FILE_NOT_FOUND: str = "Файл {filename} не найден."
ERROR_INVALID_YEAR: str = "Год публикации не может быть отрицательным или в будущем."
ERROR_INVALID_ID: str = "Ошибка: ID должно быть числом."

# Статусы книг
STATUS_AVAILABLE: str = "available"
STATUS_BORROWED: str = "borrowed"

# Сообщения статуса
STATUS_AVAILABLE_MSG: str = "✓ доступна"
STATUS_BORROWED_MSG: str = "✗ выдана до {date}"

# Меню
MENU_TITLE: str = "=== Система управления библиотекой ==="
MENU_OPTIONS: Dict[str, str] = {
    '1': 'Добавить книгу',
    '2': 'Зарегистрировать читателя',
    '3': 'Выдать книгу',
    '4': 'Вернуть книгу',
    '5': 'Поиск книг',
    '6': 'Показать все книги',
    '7': 'Показать всех читателей',
    '8': 'Проверить просроченные книги',
    '9': 'Сохранить данные',
    '10': 'Завершить',
}


class BookData(TypedDict, total=False):
    """Структура данных о книге."""
    title: str
    author: str
    year: str
    status: str
    due_date: Optional[str]


class ReaderData(TypedDict, total=False):
    """Структура данных о читателе."""
    name: str
    ticket: str
    borrowed_books: List[int]


from typing_extensions import TypedDict


class LibrarySystem:
    """
    Система управления библиотекой.

    Управляет книгами, читателями, выдачей и возвратом книг,
    а также хранением данных в JSON файле.
    """

    def __init__(self, data_file: Optional[Path] = None) -> None:
        """
        Инициализация библиотечной системы.

        Args:
            data_file: Путь к файлу данных (опционально).
        """
        self._books: Dict[int, BookData] = {}
        self._readers: Dict[int, ReaderData] = {}
        self._next_book_id: int = 1
        self._next_reader_id: int = 1
        self._fine_per_day: float = FINE_PER_DAY
        self._data_file = data_file or self._get_default_data_file()

    def _get_default_data_file(self) -> Path:
        """Получение пути к файлу данных по умолчанию."""
        project_root = Path(__file__).resolve().parent.parent
        data_dir = project_root / DATA_DIRECTORY
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir / DEFAULT_DATA_FILENAME

    def _validate_reader_id(self, reader_id: int) -> bool:
        """
        Проверка существования читателя.

        Args:
            reader_id: ID читателя.

        Returns:
            True, если читатель существует, False иначе.
        """
        if reader_id not in self._readers:
            print(ERROR_READER_NOT_FOUND)
            return False
        return True

    def _validate_book_id(self, book_id: int) -> bool:
        """
        Проверка существования книги.

        Args:
            book_id: ID книги.

        Returns:
            True, если книга существует, False иначе.
        """
        if book_id not in self._books:
            print(ERROR_BOOK_NOT_FOUND)
            return False
        return True

    def add_book(self, title: str, author: str, year: str) -> Optional[int]:
        """
        Добавление новой книги в библиотеку.

        Args:
            title: Название книги.
            author: Автор книги.
            year: Год публикации.

        Returns:
            ID добавленной книги или None, если год невалиден.
        """
        try:
            year_int = int(year)
            current_year = datetime.now().year
            if year_int < 0 or year_int > current_year + 1:
                print(ERROR_INVALID_YEAR)
                return None
        except ValueError:
            print("Ошибка: год должен быть числом.")
            return None

        book_id = self._next_book_id
        self._books[book_id] = {
            'title': title,
            'author': author,
            'year': year,
            'status': STATUS_AVAILABLE,
            'due_date': None
        }
        self._next_book_id += 1
        print(f"Книга '{title}' добавлена с ID {book_id}")
        return book_id

    def register_reader(self, name: str) -> int:
        """
        Регистрация нового читателя.

        Args:
            name: ФИО читателя.

        Returns:
            ID зарегистрированного читателя.
        """
        reader_id = self._next_reader_id
        self._readers[reader_id] = {
            'name': name,
            'ticket': f"T{reader_id:03d}",
            'borrowed_books': []
        }
        self._next_reader_id += 1
        print(f"Читатель '{name}' зарегистрирован с ID {reader_id}")
        return reader_id

    def borrow_book(self, reader_id: int, book_id: int) -> bool:
        """
        Выдача книги читателю.

        Args:
            reader_id: ID читателя.
            book_id: ID книги.

        Returns:
            True, если книга выдана, False в случае ошибки.
        """
        if not self._validate_reader_id(reader_id):
            return False

        if not self._validate_book_id(book_id):
            return False

        if self._books[book_id]['status'] != STATUS_AVAILABLE:
            print(ERROR_BOOK_ALREADY_BORROWED)
            return False

        due_date = datetime.now() + timedelta(days=LOAN_PERIOD_DAYS)
        self._books[book_id]['status'] = STATUS_BORROWED
        self._books[book_id]['due_date'] = due_date.strftime(DATE_FORMAT)
        self._readers[reader_id]['borrowed_books'].append(book_id)

        print(
            f"Книга '{self._books[book_id]['title']}' выдана читателю "
            f"'{self._readers[reader_id]['name']}' до {due_date.strftime(DISPLAY_DATE_FORMAT)}"
        )
        return True

    def return_book(self, reader_id: int, book_id: int) -> bool:
        """
        Возврат книги читателем.

        Args:
            reader_id: ID читателя.
            book_id: ID книги.

        Returns:
            True, если книга возвращена, False в случае ошибки.
        """
        if not self._validate_reader_id(reader_id):
            return False

        if not self._validate_book_id(book_id):
            return False

        if book_id not in self._readers[reader_id]['borrowed_books']:
            print(ERROR_BOOK_NOT_BORROWED_BY_READER)
            return False

        # Проверка просрочки
        today = datetime.now().date()
        due_date_str = self._books[book_id].get('due_date')
        if due_date_str:
            due_date = datetime.strptime(due_date_str, DATE_FORMAT).date()
            if today > due_date:
                days_overdue = (today - due_date).days
                fine = days_overdue * self._fine_per_day
                print(f"Книга просрочена на {days_overdue} дней. Штраф: ${fine:.2f}")
            else:
                print("Книга возвращена вовремя.")
        else:
            print("Дата возврата не определена, это ошибка.")

        self._books[book_id]['status'] = STATUS_AVAILABLE
        self._books[book_id]['due_date'] = None
        self._readers[reader_id]['borrowed_books'].remove(book_id)

        print(f"Книга '{self._books[book_id]['title']}' возвращена.")
        return True

    def search_books(self, keyword: str) -> List[int]:
        """
        Поиск книг по ключевому слову.

        Args:
            keyword: Ключевое слово для поиска.

        Returns:
            Список ID найденных книг.
        """
        print(f"\nРезультаты поиска по '{keyword}':")
        found_ids = []
        query = keyword.lower()

        for book_id, book in self._books.items():
            if (query in book['title'].lower() or
                    query in book['author'].lower()):
                status = self._get_book_status_message(book)
                print(
                    f"ID: {book_id}, '{book['title']}', {book['author']}, "
                    f"{book['year']} - {status}"
                )
                found_ids.append(book_id)

        if not found_ids:
            print("Книги не найдены")

        return found_ids

    def _get_book_status_message(self, book: BookData) -> str:
        """
        Получение строки статуса книги.

        Args:
            book: Данные книги.

        Returns:
            Строка статуса.
        """
        if book['status'] == STATUS_AVAILABLE:
            return STATUS_AVAILABLE_MSG
        else:
            return STATUS_BORROWED_MSG.format(date=book.get('due_date', '???'))

    def show_all_books(self) -> None:
        """Вывод списка всех книг в библиотеке."""
        print("\n=== Все книги в библиотеке ===")
        for book_id, book in self._books.items():
            status = self._get_book_status_message(book)
            print(
                f"ID: {book_id}, '{book['title']}', {book['author']}, "
                f"{book['year']} - {status}"
            )

    def show_all_readers(self) -> None:
        """Вывод списка всех читателей."""
        print("\n=== Все читатели ===")
        for reader_id, reader in self._readers.items():
            print(f"\nID: {reader_id}, {reader['name']}, Билет: {reader['ticket']}")
            if reader['borrowed_books']:
                print("Взятые книги:")
                for book_id in reader['borrowed_books']:
                    if book_id in self._books:
                        print(f" - {self._books[book_id]['title']}")
            else:
                print("Нет взятых книг")

    def check_overdue(self) -> List[Tuple[int, str, int]]:
        """
        Проверка просроченных книг.

        Returns:
            Список кортежей (book_id, title, days_overdue).
        """
        today = datetime.now().date()
        overdue_info = []

        for book_id, book in self._books.items():
            if book['status'] == STATUS_BORROWED:
                due_date_str = book.get('due_date')
                if due_date_str:
                    due_date = datetime.strptime(due_date_str, DATE_FORMAT).date()
                    if today > due_date:
                        days_overdue = (today - due_date).days
                        overdue_info.append((book_id, book['title'], days_overdue))

        if overdue_info:
            print("\nПросроченные книги:")
            for bid, title, days in overdue_info:
                print(f"ID {bid}: '{title}' просрочено на {days} дней.")
        else:
            print("\nНи одна книга не просрочена.")

        return overdue_info

    def save_to_file(self, filename: Optional[str] = None) -> bool:
        """
        Сохранение данных в JSON файл.

        Args:
            filename: Имя файла (опционально).

        Returns:
            True, если сохранение успешно, False в случае ошибки.
        """
        file_path = Path(filename) if filename else self._data_file

        try:
            data: Dict[str, Any] = {
                'books': self._books,
                'readers': self._readers,
                'next_book_id': self._next_book_id,
                'next_reader_id': self._next_reader_id
            }
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"Данные сохранены в {file_path}")
            return True
        except IOError as e:
            print(f"Ошибка записи файла: {e}")
            return False

    def load_from_file(self, filename: Optional[str] = None) -> bool:
        """
        Загрузка данных из JSON файла.

        Args:
            filename: Имя файла (опционально).

        Returns:
            True, если загрузка успешна, False в случае ошибки.
        """
        file_path = Path(filename) if filename else self._data_file

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self._books = data.get('books', {})
            self._readers = data.get('readers', {})
            self._next_book_id = data.get('next_book_id', 1)
            self._next_reader_id = data.get('next_reader_id', 1)
            print(f"Данные загружены из {file_path}")
            return True

        except FileNotFoundError:
            print(ERROR_FILE_NOT_FOUND.format(filename=file_path))
            return False
        except json.JSONDecodeError as e:
            print(f"Ошибка чтения JSON: {e}")
            return False


def get_int_input(prompt: str) -> Optional[int]:
    """
    Безопасный ввод целого числа.

    Args:
        prompt: Текст приглашения для ввода.

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


def print_menu() -> None:
    """Вывод меню программы."""
    print(f"\n{MENU_TITLE}")
    for key, value in MENU_OPTIONS.items():
        print(f"{key}. {value}")


def library_system() -> None:
    """
    Консольный интерфейс библиотечной системы.

    Запускает интерактивный цикл для управления библиотекой.
    """
    lib = LibrarySystem()
    lib.load_from_file()

    while True:
        print_menu()
        try:
            choice = input("Выберите действие: ").strip()
        except KeyboardInterrupt:
            print("\nРабота программы прервана.")
            lib.save_to_file()
            break

        if choice == '1':
            title = input("Введите название книги: ").strip()
            author = input("Введите автора: ").strip()
            year = input("Введите год публикации: ").strip()
            if title and author and year:
                lib.add_book(title, author, year)

        elif choice == '2':
            name = input("Введите ФИО читателя: ").strip()
            if name:
                lib.register_reader(name)

        elif choice == '3':
            reader_id = get_int_input("Введите ID читателя: ")
            book_id = get_int_input("Введите ID книги: ")
            if reader_id is not None and book_id is not None:
                lib.borrow_book(reader_id, book_id)

        elif choice == '4':
            reader_id = get_int_input("Введите ID читателя: ")
            book_id = get_int_input("Введите ID книги: ")
            if reader_id is not None and book_id is not None:
                lib.return_book(reader_id, book_id)

        elif choice == '5':
            keyword = input("Введите ключевое слово: ").strip()
            if keyword:
                lib.search_books(keyword)

        elif choice == '6':
            lib.show_all_books()

        elif choice == '7':
            lib.show_all_readers()

        elif choice == '8':
            lib.check_overdue()

        elif choice == '9':
            lib.save_to_file()

        elif choice == '10':
            lib.save_to_file()
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор.")


def main() -> None:
    """Точка входа программы."""
    library_system()


if __name__ == "__main__":
    main()

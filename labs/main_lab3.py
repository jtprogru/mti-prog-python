#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Дополнительная лабораторная работа 3.

Модуль демонстрирует:
- Анализ текста (подсчёт символов, слов, предложений)
- Функции-замыкания (make_counter)
- Операции со строками (импорт из string_operations)
- Работу с JSON (сохранение и загрузка книг)
"""

import json
import re
from datetime import datetime
from typing import Callable, Dict, List, Optional, Any

from .string_operations import (
    count_vowels,
    count_consonants,
    capitalize_words,
    remove_punctuation,
)

# Константы для форматирования таблицы книг
TABLE_COLUMN_WIDTHS: Dict[str, int] = {
    'id': 3,
    'title': 40,
    'author': 25,
    'year': 4,
}
TABLE_SEPARATOR: str = "-"

# Константы для файлов
DEFAULT_BOOKS_FILENAME: str = "books.json"

# Сообщения об ошибках
ERROR_EMPTY_AUTHOR: str = "Автор не может быть пустым"
ERROR_EMPTY_YEAR: str = "Год не может быть пустым"
ERROR_FUTURE_YEAR: str = "Год публикации не может быть в будущем (текущий год: {year})"
ERROR_FILE_SAVE: str = "Не удалось сохранить файл: {error}"
ERROR_FILE_NOT_FOUND: str = "Файл '{filename}' не найден. Возвращаем пустой список."
ERROR_INVALID_JSON: str = "Файл '{filename}' повреждён или содержит неверный JSON."
ERROR_EMPTY_LIST: str = "Список книг пуст."
ERROR_EMPTY_QUERY: str = "Запрос не введён."


class TextAnalysisResult(Dict[str, Any]):
    """Результат анализа текста."""
    pass


def analyze_text(text: str) -> TextAnalysisResult:
    """
    Анализ текста: подсчёт символов, слов, предложений.

    Args:
        text: Исходный текст для анализа.

    Returns:
        Словарь с результатами анализа:
        - characters: количество символов (включая пробелы)
        - words: количество слов
        - sentences: количество предложений
        - longest_word: самое длинное слово
    """
    characters = len(text)
    words = text.split()
    words_count = len(words)

    # Предложения считаем по точке, восклицательному и вопросительному знаку
    sentences = [s for s in re.split(r'[.!?]', text) if s.strip()]
    sentences_count = len(sentences)

    longest_word = max(words, key=len) if words else ''

    return TextAnalysisResult({
        'characters': characters,
        'words': words_count,
        'sentences': sentences_count,
        'longest_word': longest_word,
    })


def make_counter() -> Callable[[], int]:
    """
    Создание функции-счётчика.

    Returns:
        Функция, которая при каждом вызове возвращает
        увеличивающееся на 1 число.
    """
    count = 0

    def counter() -> int:
        nonlocal count
        count += 1
        return count

    return counter


def input_books() -> List[Dict[str, Any]]:
    """
    Сбор списка книг от пользователя.

    Returns:
        Список словарей с данными о книгах.
    """
    books: List[Dict[str, Any]] = []
    current_year = datetime.now().year

    print("\n=== Ввод данных о книгах ===")

    while True:
        try:
            title = input("Введите название книги (пустая строка завершает ввод): ").strip()
            if not title:
                print("Ввод завершён.")
                break

            author = input("Введите автора: ").strip()
            if not author:
                raise ValueError(ERROR_EMPTY_AUTHOR)

            year_str = input("Введите год публикации: ").strip()
            if not year_str:
                raise ValueError(ERROR_EMPTY_YEAR)

            year = int(year_str)
            if year > current_year:
                raise ValueError(ERROR_FUTURE_YEAR.format(year=current_year))

            books.append({'title': title, 'author': author, 'year': year})

        except ValueError as e:
            print(f"Ошибка: {e}. Пожалуйста, попробуйте заново.")
        except KeyboardInterrupt:
            print("\nВвод прерван пользователем.")
            break

    return books


def save_books_to_json(books: List[Dict[str, Any]], filename: str = DEFAULT_BOOKS_FILENAME) -> bool:
    """
    Сохранение списка книг в JSON файл.

    Args:
        books: Список книг для сохранения.
        filename: Имя файла для сохранения.

    Returns:
        True, если сохранение успешно, False в случае ошибки.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(books, f, ensure_ascii=False, indent=4)
        print(f"Книги сохранены в файл '{filename}'.")
        return True
    except IOError as e:
        print(ERROR_FILE_SAVE.format(error=e))
        return False


def load_books_from_json(filename: str = DEFAULT_BOOKS_FILENAME) -> List[Dict[str, Any]]:
    """
    Загрузка списка книг из JSON файла.

    Args:
        filename: Имя файла для загрузки.

    Returns:
        Список книг или пустой список в случае ошибки.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(ERROR_FILE_NOT_FOUND.format(filename=filename))
        return []
    except json.JSONDecodeError:
        print(ERROR_INVALID_JSON.format(filename=filename))
        return []


def generate_book_table_header() -> str:
    """Генерация заголовка таблицы книг."""
    widths = TABLE_COLUMN_WIDTHS
    return (
        f"{'№':<{widths['id']}} "
        f"{'Название':<{widths['title']}} "
        f"{'Автор':<{widths['author']}} "
        f"{'Год':<{widths['year']}}"
    )


def print_books_table(books: List[Dict[str, Any]]) -> None:
    """
    Вывод списка книг в виде таблицы.

    Args:
        books: Список книг для вывода.
    """
    if not books:
        print(ERROR_EMPTY_LIST)
        return

    header = generate_book_table_header()
    separator = TABLE_SEPARATOR * len(header)

    print("\n=== Список книг ===")
    print(header)
    print(separator)

    widths = TABLE_COLUMN_WIDTHS
    for idx, book in enumerate(books, start=1):
        print(
            f"{idx:<{widths['id']}} "
            f"{book['title']:<{widths['title']}} "
            f"{book['author']:<{widths['author']}} "
            f"{book['year']:<{widths['year']}}"
        )


def search_books_by_author(
    books: List[Dict[str, Any]],
    author_query: str
) -> List[Dict[str, Any]]:
    """
    Поиск книг по автору.

    Args:
        books: Список книг для поиска.
        author_query: Подстрока для поиска в имени автора.

    Returns:
        Список книг, у которых автор содержит заданную подстроку.
    """
    query = author_query.lower()
    return [
        book for book in books
        if query in book['author'].lower()
    ]


def demo_text_analysis() -> None:
    """Демонстрация анализа текста."""
    sample_text = (
        "Привет, мир! Это тестовая строка. "
        "Она содержит несколько предложений."
    )
    stats = analyze_text(sample_text)

    print("\n=== Анализ текста ===")
    for key, value in stats.items():
        print(f"{key:12}: {value}")


def demo_counter() -> None:
    """Демонстрация функции-счётчика."""
    print("\n=== Тестирование make_counter ===")
    counter1 = make_counter()
    counter2 = make_counter()

    print(f"counter1(): {counter1()}")
    print(f"counter1(): {counter1()}")
    print(f"counter2(): {counter2()}")
    print(f"counter2(): {counter2()}")


def demo_string_operations() -> None:
    """Демонстрация операций со строками."""
    print("\n=== Тестирование string_operations ===")
    text = "Hello, world! Привет, мир! 123"

    print(f"Original: {text}")
    print(f"Count vowels: {count_vowels(text)}")
    print(f"Count consonants: {count_consonants(text)}")
    print(f"Capitalized: {capitalize_words(text)}")
    print(f"Without punctuation: {remove_punctuation(text)}")


def demo_books_management() -> None:
    """Демонстрация управления книгами."""
    books = input_books()

    if books:
        save_books_to_json(books)
        loaded_books = load_books_from_json()
        print_books_table(loaded_books)

        try:
            author_query = input("\nВведите автора для поиска книг: ").strip()
            if author_query:
                found = search_books_by_author(loaded_books, author_query)
                print_books_table(found)
            else:
                print(ERROR_EMPTY_QUERY)
        except KeyboardInterrupt:
            print("\nПоиск прерван пользователем.")
    else:
        print("Книг не было введено.")


def demo() -> None:
    """
    Запуск всех демонстраций.

    Выполняет демонстрацию всех функций модуля.
    """
    demo_text_analysis()
    demo_counter()
    demo_string_operations()
    demo_books_management()


def main() -> None:
    """Точка входа программы."""
    demo()


if __name__ == "__main__":
    main()

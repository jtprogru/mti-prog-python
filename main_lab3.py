# main_lab3.py

import json
import re
from datetime import datetime
from string_operations import (
    count_vowels,
    count_consonants,
    capitalize_words,
    remove_punctuation,
)

# ------------------------------------------------------------
# 1.1. analyze_text
# ------------------------------------------------------------
def analyze_text(text: str) -> dict:
    """
    Возвращает словарь со статистикой текста:
        characters   – количество символов (включая пробелы)
        words        – количество слов
        sentences    – количество предложений (по . ! ?)
        longest_word – самое длинное слово
    """
    characters = len(text)
    words = text.split()
    words_count = len(words)

    # Предложения считаем по точке, восклицательному и вопросительному знаку
    sentences = [s for s in re.split(r'[.!?]', text) if s.strip()]
    sentences_count = len(sentences)

    longest_word = max(words, key=len) if words else ''

    return {
        'characters': characters,
        'words': words_count,
        'sentences': sentences_count,
        'longest_word': longest_word,
    }

# ------------------------------------------------------------
# 2.1. make_counter
# ------------------------------------------------------------
def make_counter():
    """Возвращает функцию‑счетчик."""
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count

    return counter

# ------------------------------------------------------------
# 4.1 + 5.1. Работа с книгами
# ------------------------------------------------------------
def input_books() -> list:
    """Собирает список книг от пользователя."""
    books = []
    print("\n=== Ввод данных о книгах ===")
    while True:
        try:
            title = input("Введите название книги (пустая строка завершает ввод): ").strip()
            if not title:
                print("Ввод завершён.")
                break

            author = input("Введите автора: ").strip()
            if not author:
                raise ValueError("Автор не может быть пустым")

            year_str = input("Введите год публикации: ").strip()
            if not year_str:
                raise ValueError("Год не может быть пустым")

            year = int(year_str)
            if year > datetime.now().year:
                raise ValueError(
                    f"Год публикации не может быть в будущем (текущий год: {datetime.now().year})"
                )

            books.append({'title': title, 'author': author, 'year': year})
        except ValueError as e:
            print(f"Ошибка: {e}. Пожалуйста, попробуйте заново.")
    return books

def save_books_to_json(books, filename='books.json'):
    """Сохраняет список книг в JSON файл."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(books, f, ensure_ascii=False, indent=4)
        print(f"Книги сохранены в файл '{filename}'.")
    except IOError as e:
        print(f"Не удалось сохранить файл: {e}")

def load_books_from_json(filename='books.json'):
    """Загружает список книг из JSON файла."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден. Возвращаем пустой список.")
        return []
    except json.JSONDecodeError:
        print(f"Файл '{filename}' повреждён или содержит неверный JSON. Возвращаем пустой список.")
        return []

def print_books_table(books):
    """Выводит список книг в виде таблицы."""
    if not books:
        print("Список книг пуст.")
        return

    header = f"{'№':<3} {'Название':<40} {'Автор':<25} {'Год':<4}"
    print("\n=== Список книг ===")
    print(header)
    print("-" * len(header))
    for idx, book in enumerate(books, start=1):
        print(f"{idx:<3} {book['title']:<40} {book['author']:<25} {book['year']:<4}")

def search_books_by_author(books, author_query):
    """Возвращает книги, у которых имя автора содержит заданную подстроку (нечувствительно к регистру)."""
    query = author_query.lower()
    return [book for book in books if query in book['author'].lower()]

# ------------------------------------------------------------
# Демонстрация всех функций
# ------------------------------------------------------------
def demo():
    # 1.1 анализ текста
    sample_text = (
        "Привет, мир! Это тестовая строка. "
        "Она содержит несколько предложений."
    )
    stats = analyze_text(sample_text)
    print("\n=== Анализ текста ===")
    for key, value in stats.items():
        print(f"{key:12}: {value}")

    # 2.1 make_counter
    print("\n=== Тестирование make_counter ===")
    counter1 = make_counter()
    counter2 = make_counter()
    print(f"counter1(): {counter1()}")
    print(f"counter1(): {counter1()}")
    print(f"counter2(): {counter2()}")
    print(f"counter2(): {counter2()}")

    # 3.1 string_operations
    print("\n=== Тестирование string_operations ===")
    text = "Hello, world! Привет, мир! 123"
    print(f"Original: {text}")
    print(f"Count vowels: {count_vowels(text)}")
    print(f"Count consonants: {count_consonants(text)}")
    print(f"Capitalized: {capitalize_words(text)}")
    print(f"Without punctuation: {remove_punctuation(text)}")

    # 4.1 + 5.1. Книги
    books = input_books()
    if books:
        save_books_to_json(books)
        loaded_books = load_books_from_json()
        print_books_table(loaded_books)

        # Поиск по автору
        author_query = input("\nВведите автора для поиска книг: ").strip()
        if author_query:
            found = search_books_by_author(loaded_books, author_query)
            print_books_table(found)
        else:
            print("Запрос не введён.")
    else:
        print("Книг не было введено.")

if __name__ == "__main__":
    demo()

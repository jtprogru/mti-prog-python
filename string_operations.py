# string_operations.py

import re
import string


def count_vowels(text: str) -> int:
    """
    Подсчитывает количество гласных букв в строке.
    Поддерживаются латинские и русские гласные.
    """
    vowels = "aeiouAEIOUаеёиоуыэюяАЕЁИОУЫЭЮЯ"
    return sum(1 for ch in text if ch in vowels)


def count_consonants(text: str) -> int:
    """
    Подсчитывает количество согласных букв в строке.
    Учитываются только буквы, не являющиеся гласными.
    """
    vowels = "aeiouAEIOUаеёиоуыэюяАЕЁИОУЫЭЮЯ"
    letters = (
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    )
    return sum(1 for ch in text if ch in letters and ch not in vowels)


def capitalize_words(text: str) -> str:
    """
    Делает первую букву каждого слова заглавной.
    """
    return ' '.join(word.capitalize() for word in text.split())


def remove_punctuation(text: str) -> str:
    """
    Удаляет все знаки препинания из строки.
    """
    # Удаляем ASCII‑знаки препинания
    translator = str.maketrans('', '', string.punctuation)
    cleaned = text.translate(translator)
    # Удаляем русские знаки препинания
    russian_punct = "«»…—‐–‚‛“”№"
    translator_ru = str.maketrans('', '', russian_punct)
    cleaned = cleaned.translate(translator_ru)
    return cleaned


def main():
    # Примерная строка для демонстрации работы функций
    sample_text = "Привет, мир! Hello, world!!!"

    # Подсчёт гласных
    vowels_count = count_vowels(sample_text)
    print(f"Исходная строка: {sample_text}")
    print(f"Количество гласных: {vowels_count}")

    # Подсчёт согласных
    consonants_count = count_consonants(sample_text)
    print(f"Количество согласных: {consonants_count}")

    # Капитализация слов
    capitalized = capitalize_words(sample_text.lower())
    print(f"Капитализация слов: {capitalized}")

    # Удаление знаков препинания
    no_punct = remove_punctuation(sample_text)
    print(f"Без знаков препинания: {no_punct}")


if __name__ == "__main__":
    main()

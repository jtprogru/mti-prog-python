#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Операции со строками.

Модуль предоставляет функции для анализа и обработки текста:
- Подсчёт гласных и согласных букв
- Капитализация слов
- Удаление знаков препинания

Поддерживаются латинские и русские буквы.
"""

import string
from typing import Set

# Гласные буквы (латинские и русские)
VOWELS: Set[str] = set("aeiouAEIOUаеёиоуыэюяАЕЁИОУЫЭЮЯ")

# Все буквы (латинские и русские)
ALL_LETTERS: Set[str] = set(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
)

# Согласные буквы (вычисляются как разность)
CONSONANTS: Set[str] = ALL_LETTERS - VOWELS

# Знаки препинания (ASCII + русские)
ASCII_PUNCTUATION: Set[str] = set(string.punctuation)
RUSSIAN_PUNCTUATION: Set[str] = set("«»…—‐–‚‛""№")
ALL_PUNCTUATION: Set[str] = ASCII_PUNCTUATION | RUSSIAN_PUNCTUATION


def count_vowels(text: str) -> int:
    """
    Подсчёт количества гласных букв в строке.

    Args:
        text: Исходная строка для анализа.

    Returns:
        Количество гласных букв.
    """
    return sum(1 for char in text if char in VOWELS)


def count_consonants(text: str) -> int:
    """
    Подсчёт количества согласных букв в строке.

    Args:
        text: Исходная строка для анализа.

    Returns:
        Количество согласных букв.
    """
    return sum(1 for char in text if char in CONSONANTS)


def capitalize_words(text: str) -> str:
    """
    Капитализация первого символа каждого слова.

    Args:
        text: Исходная строка.

    Returns:
        Строка с капитализированными словами.
    """
    if not text:
        return text
    return ' '.join(word.capitalize() for word in text.split())


def remove_punctuation(text: str) -> str:
    """
    Удаление всех знаков препинания из строки.

    Args:
        text: Исходная строка.

    Returns:
        Строка без знаков препинания.
    """
    if not text:
        return text
    return ''.join(char for char in text if char not in ALL_PUNCTUATION)


def main() -> None:
    """
    Демонстрация работы функций модуля.

    Выполняет примерную обработку строки и выводит результаты.
    """
    sample_text = "Привет, мир! Hello, world!!!"

    print(f"Исходная строка: {sample_text}")
    print(f"Количество гласных: {count_vowels(sample_text)}")
    print(f"Количество согласных: {count_consonants(sample_text)}")
    print(f"Капитализация слов: {capitalize_words(sample_text.lower())}")
    print(f"Без знаков препинания: {remove_punctuation(sample_text)}")


if __name__ == "__main__":
    main()

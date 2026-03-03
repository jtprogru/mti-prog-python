#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Анализ предложения.

Модуль анализирует введённое пользователем предложение:
- Находит самое длинное слово
- Подсчитывает частоту каждой буквы (без учёта регистра)
"""

import re
from collections import Counter
from typing import Dict, List, Optional


# Сообщения об ошибках
ERROR_EMPTY_INPUT: str = "Пустая строка."
ERROR_NO_WORDS: str = "В предложении нет слов."

# Заголовок программы
PROGRAM_TITLE: str = "=== Анализ предложения ==="


def extract_words(sentence: str) -> List[str]:
    """
    Извлечение слов из предложения.

    Args:
        sentence: Исходное предложение.

    Returns:
        Список слов (без знаков препинания).
    """
    return re.findall(r'\b\w+\b', sentence, re.UNICODE)


def extract_letters(sentence: str) -> List[str]:
    """
    Извлечение букв из предложения (в нижнем регистре).

    Args:
        sentence: Исходное предложение.

    Returns:
        Список букв в нижнем регистре.
    """
    return [char.lower() for char in sentence if char.isalpha()]


def find_longest_word(words: List[str]) -> str:
    """
    Поиск самого длинного слова в списке.

    Args:
        words: Список слов.

    Returns:
        Самое длинное слово.
    """
    return max(words, key=len)


def count_letter_frequency(letters: List[str]) -> Dict[str, int]:
    """
    Подсчёт частоты каждой буквы.

    Args:
        letters: Список букв.

    Returns:
        Словарь {буква: частота}.
    """
    return dict(Counter(letters))


def print_letter_frequency(frequency: Dict[str, int]) -> None:
    """
    Вывод частоты букв на экран.

    Args:
        frequency: Словарь частот букв.
    """
    print("\nЧастота букв:")
    for letter, count in sorted(frequency.items()):
        print(f"{letter}: {count}")


def analyze_sentence(sentence: str) -> Optional[Dict[str, object]]:
    """
    Полный анализ предложения.

    Args:
        sentence: Исходное предложение.

    Returns:
        Словарь с результатами анализа или None, если анализ невозможен.
    """
    sentence = sentence.strip()

    if not sentence:
        print(ERROR_EMPTY_INPUT)
        return None

    words = extract_words(sentence)
    if not words:
        print(ERROR_NO_WORDS)
        return None

    longest_word = find_longest_word(words)
    letters = extract_letters(sentence)
    letter_frequency = count_letter_frequency(letters)

    return {
        'longest_word': longest_word,
        'letter_frequency': letter_frequency,
    }


def print_analysis_results(results: Dict[str, object]) -> None:
    """
    Вывод результатов анализа на экран.

    Args:
        results: Словарь с результатами анализа.
    """
    print(f"Самое длинное слово: {results['longest_word']}")
    print_letter_frequency(results['letter_frequency'])  # type: ignore[arg-type]


def main() -> None:
    """
    Основная функция программы.

    Запрашивает предложение у пользователя и выводит
    результаты анализа.
    """
    print(PROGRAM_TITLE)

    try:
        sentence = input("Введите предложение: ")
    except KeyboardInterrupt:
        print("\nВвод прерван пользователем.")
        return

    results = analyze_sentence(sentence)
    if results is not None:
        print_analysis_results(results)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Сбор анкеты пользователя.

Модуль собирает базовую информацию о пользователе (имя, возраст, город, хобби)
и вычисляет примерный год рождения на основе текущего года.
"""

from datetime import datetime
from typing import Optional

# Константы для форматирования вывода
SEPARATOR_LENGTH: int = 61
SECTION_TITLE: str = "Анкета пользователя"
EQUAL_SIGN: str = "="

# Константы для валидации
MIN_AGE: int = 0
MAX_AGE: int = 150


def safe_int_input(prompt: str, min_value: Optional[int] = None, max_value: Optional[int] = None) -> Optional[int]:
    """
    Безопасный ввод целого числа с опциональной валидацией диапазона.

    Args:
        prompt: Текст приглашения для ввода.
        min_value: Минимальное допустимое значение (или None).
        max_value: Максимальное допустимое значение (или None).

    Returns:
        Введённое число или None, если ввод некорректен или вне диапазона.
    """
    try:
        value = int(input(prompt))
        if min_value is not None and value < min_value:
            print(f"Ошибка: значение должно быть не меньше {min_value}.")
            return None
        if max_value is not None and value > max_value:
            print(f"Ошибка: значение должно быть не больше {max_value}.")
            return None
        return value
    except ValueError:
        print("Ошибка: ввод должно быть целым числом.")
        return None
    except KeyboardInterrupt:
        print("\nВвод прерван пользователем.")
        return None


def calculate_birth_year(current_year: int, age: int) -> int:
    """
    Вычисление примерного года рождения.

    Args:
        current_year: Текущий год.
        age: Возраст пользователя.

    Returns:
        Примерный год рождения.
    """
    return current_year - age


def print_separator() -> None:
    """Вывод разделительной линии."""
    print(EQUAL_SIGN * SEPARATOR_LENGTH)


def print_header() -> None:
    """Вывод заголовка анкеты."""
    print()
    print_separator()
    print(f" {SECTION_TITLE} ".center(SEPARATOR_LENGTH, EQUAL_SIGN))
    print_separator()


def main() -> None:
    """
    Основная функция программы.

    Собирает анкетные данные пользователя и выводит их на экран
    вместе с вычисленным годом рождения.
    """
    print("=== Заполните анкету ===")

    # Сбор данных
    name = input("Введите ваше имя: ").strip()
    if not name:
        print("Ошибка: имя не может быть пустым.")
        return

    age = safe_int_input("Введите ваш возраст: ", min_value=MIN_AGE, max_value=MAX_AGE)
    if age is None:
        return

    city = input("Введите ваш город: ").strip()
    hobby = input("Введите ваше хобби: ").strip()

    # Вычисление года рождения
    current_year = datetime.now().year
    birth_year = calculate_birth_year(current_year, age)

    # Вывод анкеты
    print_header()
    print(f"Имя: {name}")
    print(f"Возраст: {age} лет")
    print(f"Город: {city}")
    print(f"Хобби: {hobby}")
    print(f"Примерный год рождения: {birth_year}")
    print_separator()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Лабораторная работа 1: Демонстрация типов данных, арифметики и ввода пользователя.

Модуль демонстрирует базовые типы данных Python, арифметические операции
и взаимодействие с пользователем через консольный ввод.
"""

from typing import Optional

# Демонстрационные константы
DEMO_INTEGER: int = 15
DEMO_FLOAT: float = 3.1415
DEMO_STRING: str = "Строка текста"
DEMO_BOOLEAN: bool = True

# Константы для арифметических операций
DEMO_A: int = 10
DEMO_B: int = 3


def safe_int_input(prompt: str) -> Optional[int]:
    """
    Безопасный ввод целого числа от пользователя.

    Args:
        prompt: Текст приглашения для ввода.

    Returns:
        Введённое целое число или None, если ввод некорректен.
    """
    user_input = input(prompt)
    try:
        return int(user_input)
    except ValueError:
        print(f"Ошибка: введённое значение '{user_input}' не является целым числом.")
        return None


def print_variable_info(name: str, value: object) -> None:
    """
    Вывод информации о переменной и её типе.

    Args:
        name: Имя переменной для отображения.
        value: Значение переменной.
    """
    print(f"{name}: {value} | тип: {type(value).__name__}")


def demonstrate_arithmetic(a: int, b: int) -> None:
    """
    Демонстрация арифметических операций над двумя числами.

    Args:
        a: Первое число.
        b: Второе число.
    """
    print("\nАрифметические операции:")
    print(f"a + b = {a + b}")  # сложение
    print(f"a - b = {a - b}")  # вычитание
    print(f"a * b = {a * b}")  # умножение
    print(f"a / b = {a / b}")  # обычное деление → float
    print(f"a // b = {a // b}")  # целочисленное деление → int
    print(f"a % b = {a % b}")  # остаток от деления
    print(f"a ** b = {a**b}")  # возведение в степень


def calculate_age(current_year: int, birth_year: int) -> int:
    """
    Вычисление возраста на основе текущего года и года рождения.

    Args:
        current_year: Текущий год.
        birth_year: Год рождения.

    Returns:
        Возраст в годах.
    """
    return current_year - birth_year


def main() -> None:
    """
    Основная функция программы.

    Выполняет демонстрацию типов данных, арифметических операций
    и вычисление возраста пользователя.
    """
    # 1. Приветствие
    print("Привет, мир!")

    # 2. Демонстрация переменных разных типов
    print("\nЗначения переменных и их типы:")
    print_variable_info("my_integer", DEMO_INTEGER)
    print_variable_info("my_float", DEMO_FLOAT)
    print_variable_info("my_string", DEMO_STRING)
    print_variable_info("my_boolean", DEMO_BOOLEAN)

    # 3. Арифметические операции
    demonstrate_arithmetic(DEMO_A, DEMO_B)

    # 4. Взаимодействие с пользователем
    user_name = input("\nКак вас зовут? ").strip()
    print(f"Очень приятно, {user_name}!")

    # Ввод текущего года
    year = safe_int_input("Какой сейчас год? ")
    if year is None:
        return

    # Ввод года рождения
    birth_year = safe_int_input("В каком году вы родились? ")
    if birth_year is None:
        return

    # Валидация года рождения
    if birth_year > year:
        print("Ошибка: год рождения не может быть больше текущего года.")
        return

    age = calculate_age(year, birth_year)

    # Валидация разумного возраста
    if age < 0 or age > 150:
        print(f"Ошибка: полученный возраст ({age}) выглядит нереалистично.")
        return

    print(f"В этом году вам исполнится (или уже исполнилось) {age} лет.")


if __name__ == "__main__":
    main()

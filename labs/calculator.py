#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Простой калькулятор.

Модуль выполняет базовые арифметические операции над двумя числами,
введёнными пользователем: сложение, вычитание, умножение и деление.
"""

from typing import Optional, Tuple

# Заголовок программы
PROGRAM_TITLE: str = "=== Калькулятор ==="

# Формат вывода чисел
NUMBER_FORMAT: str = "{:.2f}"


def safe_float_input(prompt: str) -> Optional[float]:
    """
    Безопасный ввод вещественного числа от пользователя.

    Args:
        prompt: Текст приглашения для ввода.

    Returns:
        Введённое число или None, если ввод некорректен.
    """
    try:
        return float(input(prompt))
    except ValueError:
        print("Ошибка: ввод должен быть числом.")
        return None
    except KeyboardInterrupt:
        print("\nВвод прерван пользователем.")
        return None


def format_number(value: float) -> str:
    """
    Форматирование числа для вывода.

    Args:
        value: Число для форматирования.

    Returns:
        Отформатированное строковое представление числа.
    """
    return NUMBER_FORMAT.format(value)


def perform_calculations(x: float, y: float) -> None:
    """
    Выполнение и вывод результатов арифметических операций.

    Args:
        x: Первое число.
        y: Второе число.
    """
    x_str = format_number(x)
    y_str = format_number(y)

    print(f"{x_str} + {y_str} = {format_number(x + y)}")
    print(f"{x_str} - {y_str} = {format_number(x - y)}")
    print(f"{x_str} * {y_str} = {format_number(x * y)}")

    if y != 0:
        print(f"{x_str} / {y_str} = {format_number(x / y)}")
    else:
        print(f"{x_str} / {y_str} = недопустимо (деление на ноль)")


def get_numbers() -> Optional[Tuple[float, float]]:
    """
    Запрос двух чисел у пользователя.

    Returns:
        Кортеж из двух чисел или None, если ввод некорректен.
    """
    x = safe_float_input("Введите первое число: ")
    if x is None:
        return None

    y = safe_float_input("Введите второе число: ")
    if y is None:
        return None

    return x, y


def main() -> None:
    """
    Основная функция программы.

    Запрашивает два числа у пользователя и выполняет
    над ними арифметические операции.
    """
    print(PROGRAM_TITLE)

    numbers = get_numbers()
    if numbers is None:
        return

    x, y = numbers
    perform_calculations(x, y)


if __name__ == "__main__":
    main()

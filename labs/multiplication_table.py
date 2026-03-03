#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Таблица умножения.

Модуль генерирует и выводит таблицу умножения от 1 до N,
где N задаётся пользователем.
"""

from typing import List, Optional

# Константы для форматирования
COLUMN_PADDING: int = 1  # Дополнительный отступ между колонками
ROW_LABEL_WIDTH: int = 3  # Ширина метки строки
HEADER_PADDING: int = 4  # Отступ для заголовка


def get_positive_integer(prompt: str) -> Optional[int]:
    """
    Запрос положительного целого числа у пользователя.

    Args:
        prompt: Текст приглашения для ввода.

    Returns:
        Положительное целое число или None, если ввод некорректен.
    """
    try:
        value = int(input(prompt))
        if value <= 0:
            print("Ошибка: число должно быть положительным.")
            return None
        return value
    except ValueError:
        print("Ошибка: введено не целое число.")
        return None
    except KeyboardInterrupt:
        print("\nВвод прерван пользователем.")
        return None


def calculate_column_width(max_value: int) -> int:
    """
    Вычисление ширины колонки для таблицы.

    Args:
        max_value: Максимальное значение в таблице.

    Returns:
        Ширина колонки с учётом padding.
    """
    return len(str(max_value)) + COLUMN_PADDING


def generate_header_row(n: int, column_width: int) -> str:
    """
    Генерация строки заголовка таблицы.

    Args:
        n: Верхняя граница таблицы.
        column_width: Ширина одной колонки.

    Returns:
        Строка заголовка таблицы.
    """
    header_parts = [f"{col:>{column_width}}" for col in range(1, n + 1)]
    return " " * HEADER_PADDING + "".join(header_parts)


def generate_data_row(row: int, n: int, column_width: int) -> str:
    """
    Генерация строки данных таблицы.

    Args:
        row: Номер текущей строки.
        n: Верхняя граница таблицы.
        column_width: Ширина одной колонки.

    Returns:
        Строка данных таблицы.
    """
    cell_parts = [f"{row * col:>{column_width}}" for col in range(1, n + 1)]
    return f"{row:>{ROW_LABEL_WIDTH}} " + "".join(cell_parts)


def print_multiplication_table(n: int) -> None:
    """
    Вывод таблицы умножения от 1 до N.

    Args:
        n: Верхняя граница таблицы.
    """
    max_value = n * n
    column_width = calculate_column_width(max_value)

    # Вывод заголовка
    print(generate_header_row(n, column_width))

    # Вывод строк данных
    for row in range(1, n + 1):
        print(generate_data_row(row, n, column_width))


def main() -> None:
    """
    Основная функция программы.

    Запрашивает верхнюю границу таблицы у пользователя
    и выводит таблицу умножения.
    """
    print("=== Таблица умножения ===")

    n = get_positive_integer("Введите N (верхняя граница таблицы): ")
    if n is None:
        return

    print_multiplication_table(n)


if __name__ == "__main__":
    main()

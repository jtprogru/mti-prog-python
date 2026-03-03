#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Определение типа треугольника по длинам сторон.

Модуль запрашивает у пользователя длины трёх сторон треугольника,
проверяет существование треугольника и определяет его тип:
равносторонний, равнобедренный или разносторонний.
"""

from typing import Optional, Tuple

# Сообщения об ошибках
ERROR_INVALID_NUMBER: str = "Ошибка: введено не число."
ERROR_INVALID_SIDE: str = "Не треугольник (недопустимая сторона)"
ERROR_NOT_TRIANGLE: str = "Не треугольник (сумма двух сторон меньше третьей)"

# Типы треугольников
TYPE_EQUILATERAL: str = "Равносторонний треугольник"
TYPE_ISOSCELES: str = "Равнобедренный треугольник"
TYPE_SCALENE: str = "Разносторонний треугольник"


def get_side_length(side_name: str) -> Optional[float]:
    """
    Запрос длины стороны треугольника у пользователя.

    Args:
        side_name: Название стороны для отображения в приглашении.

    Returns:
        Длина стороны или None, если ввод некорректен.
    """
    try:
        return float(input(f"Введите длину {side_name}: "))
    except ValueError:
        print(ERROR_INVALID_NUMBER)
        return None
    except KeyboardInterrupt:
        print("\nВвод прерван пользователем.")
        return None


def is_valid_triangle(a: float, b: float, c: float) -> Tuple[bool, Optional[str]]:
    """
    Проверка существования треугольника по длинам сторон.

    Args:
        a: Длина первой стороны.
        b: Длина второй стороны.
        c: Длина третьей стороны.

    Returns:
        Кортеж (валиден, ошибка):
        - (True, None) если треугольник валиден
        - (False, сообщение) если треугольник невалиден
    """
    if a <= 0 or b <= 0 or c <= 0:
        return False, ERROR_INVALID_SIDE

    if (a + b <= c) or (a + c <= b) or (b + c <= a):
        return False, ERROR_NOT_TRIANGLE

    return True, None


def get_triangle_type(a: float, b: float, c: float) -> str:
    """
    Определение типа треугольника по длинам сторон.

    Предполагается, что треугольник уже проверен на валидность.

    Args:
        a: Длина первой стороны.
        b: Длина второй стороны.
        c: Длина третьей стороны.

    Returns:
        Строковое описание типа треугольника.
    """
    if a == b == c:
        return TYPE_EQUILATERAL
    elif a == b or a == c or b == c:
        return TYPE_ISOSCELES
    else:
        return TYPE_SCALENE


def get_triangle_sides() -> Optional[Tuple[float, float, float]]:
    """
    Запрос всех трёх сторон треугольника у пользователя.

    Returns:
        Кортеж из трёх длин сторон или None, если ввод некорректен.
    """
    a = get_side_length("первой стороны")
    if a is None:
        return None

    b = get_side_length("второй стороны")
    if b is None:
        return None

    c = get_side_length("третьей стороны")
    if c is None:
        return None

    return a, b, c


def determine_triangle_type() -> None:
    """
    Основная логика определения типа треугольника.

    Запрашивает длины сторон, проверяет валидность треугольника
    и выводит его тип.
    """
    print("=== Определение типа треугольника ===")

    sides = get_triangle_sides()
    if sides is None:
        return

    a, b, c = sides

    is_valid, error = is_valid_triangle(a, b, c)
    if not is_valid:
        print(error)
        return

    triangle_type = get_triangle_type(a, b, c)
    print(triangle_type)


def main() -> None:
    """Точка входа программы."""
    determine_triangle_type()


if __name__ == "__main__":
    main()

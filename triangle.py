#!/usr/bin/env python


def triangle_type():
    print("=== Определение типа треугольника ===")
    try:
        a = float(input("Введите длину первой стороны: "))
        b = float(input("Введите длину второй стороны: "))
        c = float(input("Введите длину третьей стороны: "))
    except ValueError:
        print("Ошибка: введено не число.")
        return

    # Проверка треугольника
    if a <= 0 or b <= 0 or c <= 0:
        print("Не треугольник (недопустимая сторона)")
        return

    if a + b <= c or a + c <= b or b + c <= a:
        print("Не треугольник (сумма двух сторон меньше третьей)")
        return

    # Определяем тип
    if a == b == c:
        print("Равносторонний треугольник")
    elif a == b or a == c or b == c:
        print("Равнобедренный треугольник")
    else:
        print("Разносторонний треугольник")


if __name__ == "__main__":
    triangle_type()

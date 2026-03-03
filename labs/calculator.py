#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def main():
    print("=== Калькулятор ===")
    try:
        x = float(input("Введите первое число: "))
        y = float(input("Введите второе число: "))
    except ValueError:
        print("Ошибка: ввод должен быть числом.")
        return

    print(f"{x} + {y} = {x + y}")
    print(f"{x} - {y} = {x - y}")
    print(f"{x} * {y} = {x * y}")
    if y != 0:
        print(f"{x} / {y} = {x / y}")
    else:
        print(f"{x} / {y} = недопустимо (деление на ноль)")


if __name__ == "__main__":
    main()

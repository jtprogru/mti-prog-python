#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Лабораторная работа 1
"""


def main():
    # 1. Привет, мир!
    print("Привет, мир!")

    # 2. Переменные разных типов
    my_integer = 15  # int
    my_float = 3.1415  # float
    my_string = "Строка текста"  # str
    my_boolean = True  # bool

    print("\nЗначения переменных и их типы:")
    print(f"my_integer: {my_integer} | тип: {type(my_integer)}")
    print(f"my_float:   {my_float}   | тип: {type(my_float)}")
    print(f"my_string:  {my_string} | тип: {type(my_string)}")
    print(f"my_boolean: {my_boolean} | тип: {type(my_boolean)}")

    # 3. Арифметические операции
    a = 10
    b = 3

    print("\nАрифметические операции:")
    print(f"a + b = {a + b}")  # сложение
    print(f"a - b = {a - b}")  # вычитание
    print(f"a * b = {a * b}")  # умножение
    print(f"a / b = {a / b}")  # обычное деление → float
    print(f"a // b = {a // b}")  # целочисленное деление → int
    print(f"a % b = {a % b}")  # остаток от деления
    print(f"a ** b = {a**b}")  # возведение в степень

    # 4. Взаимодействие с пользователем
    user_name = input("\nКак вас зовут? ")
    print(f"Очень приятно, {user_name}!")

    year_str = input("Какой сейчас год? ")
    try:
        year = int(year_str)
    except ValueError:
        print("Ошибка: год должен быть целым числом.")
        return

    birth_year_str = input("В каком году вы родились? ")
    try:
        birth_year = int(birth_year_str)
    except ValueError:
        print("Ошибка: год рождения должен быть целым числом.")
        return

    age = year - birth_year
    print(f"В этом году вам исполнится (или уже исполнилось) {age} лет.")


if __name__ == "__main__":
    main()

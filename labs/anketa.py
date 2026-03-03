#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime


def main():
    print("=== Заполните анкету ===")
    name = input("Введите ваше имя: ")

    age_str = input("Введите ваш возраст: ")
    try:
        age = int(age_str)
    except ValueError:
        print("Ошибка: возраст должен быть целым числом.")
        return

    city = input("Введите ваш город: ")
    hobby = input("Введите ваше хобби: ")

    current_year = datetime.now().year
    birth_year = current_year - age

    print("\n" + "=" * 20 + " Анкета пользователя " + "=" * 20)
    print(f"Имя: {name}")
    print(f"Возраст: {age} лет")
    print(f"Город: {city}")
    print(f"Хобби: {hobby}")
    print(f"Примерный год рождения: {birth_year}")
    print("=" * 61)


if __name__ == "__main__":
    main()

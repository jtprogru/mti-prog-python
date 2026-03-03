#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Точка входа проекта mti-prog-python.

Модуль предоставляет основную функцию для запуска проекта
и информацию о доступных лабораторных работах.
"""


def main() -> None:
    """
    Основная функция проекта.

    Выводит приветственное сообщение и список доступных
    лабораторных работ для запуска.
    """
    print("Hello from mti-prog-python!")
    print("*" * 10)
    print("\nДля проверки выполнять запуск отдельных файлов:")
    print("  python -m labs.lab1")
    print("  python -m labs.calculator")
    print("  python -m labs.anketa")
    print("  и т.д.")
    print("\nДоступные лабораторные работы:")
    print("  - lab1: Типы данных и арифметика")
    print("  - calculator: Простой калькулятор")
    print("  - anketa: Анкета пользователя")
    print("  - triangle: Определение типа треугольника")
    print("  - multiplication_table: Таблица умножения")
    print("  - sentence_analysis: Анализ предложения")
    print("  - student_grades: Оценки студентов")
    print("  - inventory: Учёт инвентаря")
    print("  - library_system: Библиотечная система")
    print("  - main_lab3: Дополнительная лабораторная")
    print("  - string_operations: Операции со строками")
    print("  - diary_app: Приложение-ежедневник")


if __name__ == "__main__":
    main()

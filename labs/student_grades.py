#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Система учёта оценок студентов.

Модуль предоставляет класс StudentGrades для управления студентами
и их оценками, а также консольный интерфейс для взаимодействия.
"""

from typing import Dict, List, Optional, Tuple

# Константы для валидации оценок
MIN_GRADE: float = 0.0
MAX_GRADE: float = 100.0

# Сообщения об ошибках
ERROR_STUDENT_EXISTS: str = "Студент {name} уже существует."
ERROR_STUDENT_NOT_FOUND: str = "Студент {name} не найден."
ERROR_INVALID_GRADE: str = "Ошибка: оценка должна быть числом от {min} до {max}."
ERROR_NO_GRADES: str = "Нет оценок для {name}."
ERROR_NO_STUDENTS: str = "Нет студентов с оценками."

# Сообщения меню
MENU_TITLE: str = "=== Система оценок студентов ==="
MENU_OPTIONS: Dict[str, str] = {
    '1': 'Добавить студента',
    '2': 'Добавить оценку',
    '3': 'Удалить студента',
    '4': 'Показать средний балл студента',
    '5': 'Показать всех студентов со средними баллами',
    '6': 'Найти студента с самым высоким средним баллом',
    '7': 'Выход',
}


class StudentGrades:
    """
    Класс для управления студентами и их оценками.

    Хранит информацию о студентах и их оценках, предоставляет методы
    для добавления, удаления студентов и управления оценками.
    """

    def __init__(self) -> None:
        """Инициализация пустой системы оценок."""
        self._grades: Dict[str, List[float]] = {}

    def add_student(self, name: str) -> bool:
        """
        Добавление нового студента.

        Args:
            name: Имя студента.

        Returns:
            True, если студент добавлен, False если уже существует.
        """
        if name in self._grades:
            print(ERROR_STUDENT_EXISTS.format(name=name))
            return False

        self._grades[name] = []
        print(f"Добавлен студент {name}.")
        return True

    def add_grade(self, name: str, grade: float) -> bool:
        """
        Добавление оценки студенту.

        Args:
            name: Имя студента.
            grade: Оценка для добавления.

        Returns:
            True, если оценка добавлена, False в случае ошибки.
        """
        if name not in self._grades:
            print(ERROR_STUDENT_NOT_FOUND.format(name=name))
            return False

        if not (MIN_GRADE <= grade <= MAX_GRADE):
            print(ERROR_INVALID_GRADE.format(min=MIN_GRADE, max=MAX_GRADE))
            return False

        self._grades[name].append(grade)
        print(f"Добавлена оценка {grade:.2f} для {name}.")
        return True

    def delete_student(self, name: str) -> bool:
        """
        Удаление студента из системы.

        Args:
            name: Имя студента для удаления.

        Returns:
            True, если студент удалён, False если не найден.
        """
        if name not in self._grades:
            print(ERROR_STUDENT_NOT_FOUND.format(name=name))
            return False

        del self._grades[name]
        print(f"Удалён студент {name}.")
        return True

    def _calculate_average(self, name: str) -> Optional[float]:
        """
        Вычисление среднего балла студента.

        Args:
            name: Имя студента.

        Returns:
            Средний балл или None, если оценок нет.
        """
        grades = self._grades.get(name, [])
        if not grades:
            return None
        return sum(grades) / len(grades)

    def get_average_grade(self, name: str) -> Optional[float]:
        """
        Получение и вывод среднего балла студента.

        Args:
            name: Имя студента.

        Returns:
            Средний балл или None, если оценок нет.
        """
        if name not in self._grades:
            print(ERROR_STUDENT_NOT_FOUND.format(name=name))
            return None

        avg = self._calculate_average(name)
        if avg is None:
            print(ERROR_NO_GRADES.format(name=name))
            return None

        print(f"Средняя оценка для {name}: {avg:.2f}")
        return avg

    def get_all_averages(self) -> List[Tuple[str, Optional[float]]]:
        """
        Получение списка всех студентов и их средних баллов.

        Returns:
            Список кортежей (имя, средний_балл).
        """
        result = []
        for name, grades in self._grades.items():
            if grades:
                avg = sum(grades) / len(grades)
                result.append((name, avg))
            else:
                result.append((name, None))
        return result

    def print_all_averages(self) -> None:
        """Вывод списка всех студентов и их средних баллов."""
        print("Список студентов и их средние баллы:")
        for name, avg in self.get_all_averages():
            if avg is not None:
                print(f"{name}: {avg:.2f}")
            else:
                print(f"{name}: нет оценок")

    def get_top_student(self) -> Optional[Tuple[str, float]]:
        """
        Поиск студента с самым высоким средним баллом.

        Returns:
            Кортеж (имя, средний_балл) или None, если нет студентов с оценками.
        """
        best_name: Optional[str] = None
        best_avg: float = -1.0

        for name, grades in self._grades.items():
            if grades:
                avg = sum(grades) / len(grades)
                if avg > best_avg:
                    best_avg = avg
                    best_name = name

        if best_name is None:
            return None
        return best_name, best_avg

    def print_top_student(self) -> None:
        """Вывод информации о лучшем студенте."""
        result = self.get_top_student()
        if result is not None:
            name, avg = result
            print(f"Лучший студент: {name} со средним баллом {avg:.2f}")
        else:
            print(ERROR_NO_STUDENTS)


def get_float_input(prompt: str) -> Optional[float]:
    """
    Безопасный ввод вещественного числа.

    Args:
        prompt: Текст приглашения для ввода.

    Returns:
        Введённое число или None, если ввод некорректен.
    """
    try:
        return float(input(prompt).strip())
    except ValueError:
        print(ERROR_INVALID_GRADE.format(min=MIN_GRADE, max=MAX_GRADE))
        return None
    except KeyboardInterrupt:
        print("\nВвод прерван пользователем.")
        return None


def print_menu() -> None:
    """Вывод меню программы."""
    print(f"\n{MENU_TITLE}")
    for key, value in MENU_OPTIONS.items():
        print(f"{key}. {value}")


def student_grades_system() -> None:
    """
    Консольный интерфейс системы оценок.

    Запускает интерактивный цикл для управления студентами и оценками.
    """
    system = StudentGrades()

    while True:
        print_menu()
        try:
            choice = input("Выберите действие: ").strip()
        except KeyboardInterrupt:
            print("\nРабота программы прервана.")
            break

        if choice == '1':
            name = input("Введите имя студента: ").strip()
            if name:
                system.add_student(name)

        elif choice == '2':
            name = input("Введите имя студента: ").strip()
            grade = get_float_input("Введите оценку: ")
            if grade is not None:
                system.add_grade(name, grade)

        elif choice == '3':
            name = input("Введите имя студента: ").strip()
            system.delete_student(name)

        elif choice == '4':
            name = input("Введите имя студента: ").strip()
            system.get_average_grade(name)

        elif choice == '5':
            system.print_all_averages()

        elif choice == '6':
            system.print_top_student()

        elif choice == '7':
            break

        else:
            print("Неверный выбор.")


def main() -> None:
    """Точка входа программы."""
    student_grades_system()


if __name__ == "__main__":
    main()

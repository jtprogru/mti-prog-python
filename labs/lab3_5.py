#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Лабораторная работа №4: Объектно-ориентированное программирование (ООП)

Модуль содержит решения всех заданий по ООП:
- Задание 1.1: Класс Book
- Задание 2.1: Класс Student с инкапсуляцией
- Задание 3.1: Классы Shape, Rectangle, Circle, Square
- Задание 4.1: Класс Matrix с перегрузкой операторов
- Задание 5.1: Класс-методы и статические методы в Book
- Задание 6.1: Класс Library с композицией
"""

from datetime import datetime
from typing import List, Dict, Any
from copy import deepcopy
import math


# =============================================================================
# Задание 1.1 + 5.1: Класс Book
# =============================================================================

class Book:
    """
    Класс, представляющий книгу.
    
    Атрибуты:
        title: Название книги.
        author: Автор книги.
        year: Год издания.
        is_available: Статус доступности (True/False).
    """
    
    def __init__(self, title: str, author: str, year: int, is_available: bool = True):
        """
        Конструктор класса Book.
        
        Args:
            title: Название книги.
            author: Автор книги.
            year: Год издания.
            is_available: Статус доступности (по умолчанию True).
        """
        self.title = title
        self.author = author
        self.year = year
        self.is_available = is_available
    
    def borrow(self) -> bool:
        """
        Взять книгу (изменить статус на недоступна).
        
        Returns:
            True, если книга успешно взята, False если уже недоступна.
        """
        if self.is_available:
            self.is_available = False
            print(f"Книга '{self.title}' взята.")
            return True
        else:
            print(f"Книга '{self.title}' уже недоступна.")
            return False
    
    def return_book(self) -> None:
        """Вернуть книгу (изменить статус на доступна)."""
        self.is_available = True
        print(f"Книга '{self.title}' возвращена.")
    
    def get_info(self) -> str:
        """
        Получить информацию о книге.
        
        Returns:
            Строка с информацией о книге.
        """
        status = "доступна" if self.is_available else "недоступна"
        return f"'{self.title}' - {self.author} ({self.year}), статус: {status}"
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Book':
        """
        Класс-метод для создания книги из словаря.
        
        Args:
            data: Словарь с данными книги (title, author, year, is_available).
        
        Returns:
            Новый объект Book.
        """
        return cls(
            title=data.get('title', 'Без названия'),
            author=data.get('author', 'Неизвестный'),
            year=data.get('year', datetime.now().year),
            is_available=data.get('is_available', True)
        )
    
    @staticmethod
    def is_valid_year(year: int) -> bool:
        """
        Статический метод для проверки года издания.
        
        Args:
            year: Год для проверки.
        
        Returns:
            True, если год не больше текущего, иначе False.
        """
        current_year = datetime.now().year
        return year <= current_year
    
    def __str__(self) -> str:
        """Строковое представление для пользователя."""
        return self.get_info()
    
    def __repr__(self) -> str:
        """Официальное представление для разработчика."""
        return f"Book('{self.title}', '{self.author}', {self.year}, {self.is_available})"


# =============================================================================
# Задание 2.1: Класс Student с инкапсуляцией
# =============================================================================

class Student:
    """
    Класс, представляющий студента.
    
    Атрибуты:
        __name: Имя студента (приватный).
        __grades: Список оценок (приватный).
    """
    
    def __init__(self, name: str):
        """
        Конструктор класса Student.
        
        Args:
            name: Имя студента.
        """
        self.__name = name
        self.__grades: List[int] = []
    
    def add_grade(self, grade: int) -> bool:
        """
        Добавить оценку.
        
        Args:
            grade: Оценка (от 2 до 5).
        
        Returns:
            True, если оценка добавлена, False если неверная оценка.
        """
        if 2 <= grade <= 5:
            self.__grades.append(grade)
            print(f"Оценка {grade} добавлена для студента {self.__name}.")
            return True
        else:
            print(f"Ошибка: оценка должна быть от 2 до 5 (получено {grade}).")
            return False
    
    def average_grade(self) -> float:
        """
        Вычислить средний балл.
        
        Returns:
            Среднее значение оценок или 0.0, если оценок нет.
        """
        if not self.__grades:
            return 0.0
        return sum(self.__grades) / len(self.__grades)
    
    @property
    def name(self) -> str:
        """Геттер для имени (только чтение)."""
        return self.__name
    
    @property
    def grades(self) -> List[int]:
        """Геттер для оценок (только чтение, возвращает копию)."""
        return deepcopy(self.__grades)
    
    def __str__(self) -> str:
        """Строковое представление студента."""
        avg = self.average_grade()
        return f"Student('{self.__name}', оценок: {len(self.__grades)}, средний балл: {avg:.2f})"


# =============================================================================
# Задание 3.1: Классы Shape, Rectangle, Circle, Square
# =============================================================================

class Shape:
    """Базовый класс для геометрических фигур."""
    
    def area(self) -> float:
        """
        Вычислить площадь фигуры.
        
        Returns:
            Площадь фигуры (по умолчанию 0).
        """
        return 0.0


class Rectangle(Shape):
    """
    Класс прямоугольника.
    
    Атрибуты:
        width: Ширина.
        height: Высота.
    """
    
    def __init__(self, width: float, height: float):
        """
        Конструктор прямоугольника.
        
        Args:
            width: Ширина прямоугольника.
            height: Высота прямоугольника.
        """
        self.width = width
        self.height = height
    
    def area(self) -> float:
        """
        Вычислить площадь прямоугольника.
        
        Returns:
            Площадь = width * height.
        """
        return self.width * self.height
    
    def __str__(self) -> str:
        return f"Rectangle(width={self.width}, height={self.height}, area={self.area()})"


class Circle(Shape):
    """
    Класс круга.
    
    Атрибуты:
        radius: Радиус.
    """
    
    def __init__(self, radius: float):
        """
        Конструктор круга.
        
        Args:
            radius: Радиус круга.
        """
        self.radius = radius
    
    def area(self) -> float:
        """
        Вычислить площадь круга.
        
        Returns:
            Площадь = π * r².
        """
        return math.pi * self.radius ** 2
    
    def __str__(self) -> str:
        return f"Circle(radius={self.radius}, area={self.area():.2f})"


class Square(Rectangle):
    """
    Класс квадрата (наследуется от Rectangle).
    
    Атрибуты:
        side: Длина стороны.
    """
    
    def __init__(self, side: float):
        """
        Конструктор квадрата.
        
        Args:
            side: Длина стороны квадрата.
        """
        super().__init__(side, side)
        self.side = side
    
    def __str__(self) -> str:
        return f"Square(side={self.side}, area={self.area()})"


# =============================================================================
# Задание 4.1: Класс Matrix с перегрузкой операторов
# =============================================================================

class Matrix:
    """
    Класс матрицы 2x2.
    
    Атрибуты:
        data: Двумерный список 2x2 с элементами матрицы.
    """
    
    def __init__(self, a: float, b: float, c: float, d: float):
        """
        Конструктор матрицы 2x2.
        
        Args:
            a: Элемент [0][0].
            b: Элемент [0][1].
            c: Элемент [1][0].
            d: Элемент [1][1].
        """
        self.data = [[a, b], [c, d]]
    
    def __repr__(self) -> str:
        """Официальное строковое представление."""
        return f"Matrix({self.data[0][0]}, {self.data[0][1]}, {self.data[1][0]}, {self.data[1][1]})"
    
    def __str__(self) -> str:
        """Неформальное строковое представление."""
        return f"[{self.data[0][0]}, {self.data[0][1]}]\n[{self.data[1][0]}, {self.data[1][1]}]"
    
    def __add__(self, other: 'Matrix') -> 'Matrix':
        """Перегрузка оператора сложения +."""
        return Matrix(
            self.data[0][0] + other.data[0][0],
            self.data[0][1] + other.data[0][1],
            self.data[1][0] + other.data[1][0],
            self.data[1][1] + other.data[1][1]
        )
    
    def __sub__(self, other: 'Matrix') -> 'Matrix':
        """Перегрузка оператора вычитания -."""
        return Matrix(
            self.data[0][0] - other.data[0][0],
            self.data[0][1] - other.data[0][1],
            self.data[1][0] - other.data[1][0],
            self.data[1][1] - other.data[1][1]
        )
    
    def __mul__(self, other: 'Matrix') -> 'Matrix':
        """
        Перегрузка оператора умножения *.
        Умножение матриц по правилам линейной алгебры.
        """
        a, b = self.data[0]
        c, d = self.data[1]
        e, f = other.data[0]
        g, h = other.data[1]
        
        return Matrix(
            a * e + b * g,  # [0][0]
            a * f + b * h,  # [0][1]
            c * e + d * g,  # [1][0]
            c * f + d * h   # [1][1]
        )
    
    def __eq__(self, other: 'Matrix') -> bool:
        """Проверка на равенство матриц."""
        return (
            self.data[0][0] == other.data[0][0] and
            self.data[0][1] == other.data[0][1] and
            self.data[1][0] == other.data[1][0] and
            self.data[1][1] == other.data[1][1]
        )
    
    def determinant(self) -> float:
        """
        Вычислить определитель матрицы.
        
        Returns:
            Определитель = ad - bc.
        """
        return self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0]


# =============================================================================
# Задание 6.1: Класс Library с композицией
# =============================================================================

class Library:
    """
    Класс библиотеки, содержащий список книг.
    
    Атрибуты:
        name: Название библиотеки.
        books: Список книг.
    """
    
    def __init__(self, name: str):
        """
        Конструктор библиотеки.
        
        Args:
            name: Название библиотеки.
        """
        self.name = name
        self.books: List[Book] = []
    
    def add_book(self, book: Book) -> None:
        """
        Добавить книгу в библиотеку.
        
        Args:
            book: Объект книги для добавления.
        """
        self.books.append(book)
        print(f"Книга '{book.title}' добавлена в библиотеку '{self.name}'.")
    
    def remove_book(self, title: str) -> bool:
        """
        Удалить книгу по названию.
        
        Args:
            title: Название книги для удаления.
        
        Returns:
            True, если книга удалена, False если не найдена.
        """
        for i, book in enumerate(self.books):
            if book.title == title:
                removed = self.books.pop(i)
                print(f"Книга '{removed.title}' удалена из библиотеки.")
                return True
        print(f"Книга '{title}' не найдена в библиотеке.")
        return False
    
    def find_by_author(self, author_name: str) -> List[Book]:
        """
        Найти книги по автору.
        
        Args:
            author_name: Имя автора для поиска.
        
        Returns:
            Список книг указанного автора.
        """
        found = [
            book for book in self.books
            if author_name.lower() in book.author.lower()
        ]
        if found:
            print(f"Найдено книг автора '{author_name}': {len(found)}")
        else:
            print(f"Книги автора '{author_name}' не найдены.")
        return found
    
    def borrow_book(self, title: str) -> bool:
        """
        Взять книгу из библиотеки.
        
        Args:
            title: Название книги.
        
        Returns:
            True, если книга взята, False если не найдена или недоступна.
        """
        for book in self.books:
            if book.title == title:
                return book.borrow()
        print(f"Книга '{title}' не найдена в библиотеке.")
        return False
    
    def return_book(self, title: str) -> None:
        """
        Вернуть книгу в библиотеку.
        
        Args:
            title: Название книги.
        """
        for book in self.books:
            if book.title == title:
                book.return_book()
                return
        print(f"Книга '{title}' не найдена в библиотеке.")
    
    def list_books(self) -> None:
        """Вывести список всех книг в библиотеке."""
        print(f"\n=== Библиотека '{self.name}' ===")
        if not self.books:
            print("Список книг пуст.")
            return
        
        for i, book in enumerate(self.books, 1):
            print(f"{i}. {book.get_info()}")
    
    def __len__(self) -> int:
        """Количество книг в библиотеке."""
        return len(self.books)
    
    def __str__(self) -> str:
        return f"Library('{self.name}', книг: {len(self.books)})"


# =============================================================================
# Демонстрация работы
# =============================================================================

def demo_book() -> None:
    """Демонстрация работы с классом Book."""
    print("\n" + "=" * 60)
    print("ЗАДАНИЕ 1.1 + 5.1: Класс Book")
    print("=" * 60)
    
    # Создание книг
    book1 = Book("Война и мир", "Лев Толстой", 1869)
    book2 = Book("Преступление и наказание", "Фёдор Достоевский", 1866, is_available=False)
    
    print(book1.get_info())
    print(book2.get_info())
    
    # Методы borrow и return_book
    book1.borrow()
    book1.borrow()  # Повторная попытка
    book1.return_book()
    
    # Проверка статического метода
    print(f"\nПроверка года 1869: {Book.is_valid_year(1869)}")
    print(f"Проверка года 2050: {Book.is_valid_year(2050)}")
    
    # Класс-метод from_dict
    book_data = {"title": "Анна Каренина", "author": "Лев Толстой", "year": 1877}
    book3 = Book.from_dict(book_data)
    print(f"\nКнига из словаря: {book3}")


def demo_student() -> None:
    """Демонстрация работы с классом Student."""
    print("\n" + "=" * 60)
    print("ЗАДАНИЕ 2.1: Класс Student с инкапсуляцией")
    print("=" * 60)
    
    student = Student("Иван Петров")
    
    # Добавление оценок
    student.add_grade(5)
    student.add_grade(4)
    student.add_grade(5)
    student.add_grade(6)  # Неверная оценка
    
    # Вывод информации
    print(f"\nСтудент: {student.name}")
    print(f"Оценки: {student.grades}")
    print(f"Средний балл: {student.average_grade():.2f}")
    
    # Попытка изменить приватный атрибут (не сработает)
    print("\nПопытка изменить оценки напрямую...")
    student.grades.append(2)  # Это изменит копию, а не оригинал
    print(f"Оценки после 'изменения': {student.grades}")


def demo_shapes() -> None:
    """Демонстрация работы с геометрическими фигурами."""
    print("\n" + "=" * 60)
    print("ЗАДАНИЕ 3.1: Классы Shape, Rectangle, Circle, Square")
    print("=" * 60)
    
    # Базовый класс
    shape = Shape()
    print(f"Shape area: {shape.area()}")
    
    # Прямоугольник
    rect = Rectangle(5, 3)
    print(f"Rectangle: {rect}")
    
    # Круг
    circle = Circle(4)
    print(f"Circle: {circle}")
    
    # Квадрат
    square = Square(5)
    print(f"Square: {square}")
    
    # Полиморфизм
    shapes = [Rectangle(2, 3), Circle(5), Square(4)]
    print("\nПолиморфизм:")
    for s in shapes:
        print(f"  {s.__class__.__name__}: площадь = {s.area():.2f}")


def demo_matrix() -> None:
    """Демонстрация работы с матрицами."""
    print("\n" + "=" * 60)
    print("ЗАДАНИЕ 4.1: Класс Matrix с перегрузкой операторов")
    print("=" * 60)
    
    m1 = Matrix(1, 2, 3, 4)
    m2 = Matrix(5, 6, 7, 8)
    
    print(f"Matrix 1:\n{m1}")
    print(f"\nMatrix 2:\n{m2}")
    
    print(f"\nMatrix 1 + Matrix 2:\n{m1 + m2}")
    print(f"\nMatrix 2 - Matrix 1:\n{m2 - m1}")
    print(f"\nMatrix 1 * Matrix 2:\n{m1 * m2}")
    
    print(f"\nОпределитель m1: {m1.determinant()}")
    print(f"Определитель m2: {m2.determinant()}")
    
    # Проверка равенства
    m3 = Matrix(1, 2, 3, 4)
    print(f"\nm1 == m3: {m1 == m3}")
    print(f"m1 == m2: {m1 == m2}")


def demo_library() -> None:
    """Демонстрация работы с библиотекой."""
    print("\n" + "=" * 60)
    print("ЗАДАНИЕ 6.1: Класс Library")
    print("=" * 60)
    
    # Создание библиотеки
    library = Library("Городская библиотека")
    
    # Добавление книг
    library.add_book(Book("Война и мир", "Лев Толстой", 1869))
    library.add_book(Book("Анна Каренина", "Лев Толстой", 1877))
    library.add_book(Book("Преступление и наказание", "Фёдор Достоевский", 1866))
    library.add_book(Book("Братья Карамазовы", "Фёдор Достоевский", 1880))
    
    # Список книг
    library.list_books()
    
    # Поиск по автору
    print("\n--- Поиск книг Льва Толстого ---")
    library.find_by_author("Лев Толстой")
    
    # Взять и вернуть книгу
    print("\n--- Взятие книги ---")
    library.borrow_book("Война и мир")
    library.borrow_book("Война и мир")  # Повторная попытка
    
    print("\n--- Возврат книги ---")
    library.return_book("Война и мир")
    
    # Удаление книги
    print("\n--- Удаление книги ---")
    library.remove_book("Анна Каренина")
    
    # Финальный список
    library.list_books()
    print(f"\n{library}")


def demo() -> None:
    """Запуск всех демонстраций."""
    print("\n" + "=" * 60)
    print("ЛАБОРАТОРНАЯ РАБОТА №4: ОБЪЕКТНО-ОРИЕНТИРОВАННОЕ ПРОГРАММИРОВАНИЕ")
    print("=" * 60)
    
    demo_book()
    demo_student()
    demo_shapes()
    demo_matrix()
    demo_library()
    
    print("\n" + "=" * 60)
    print("ВСЕ ЗАДАНИЯ ВЫПОЛНЕНЫ УСПЕШНО!")
    print("=" * 60)


def main() -> None:
    """Точка входа программы."""
    demo()


if __name__ == "__main__":
    main()

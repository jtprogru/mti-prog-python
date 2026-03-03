#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Система учёта инвентаря.

Модуль предоставляет класс Inventory для управления товарами,
их количеством, ценой и категориями.
"""

from typing import Dict, Optional, Set, Tuple, List
from typing_extensions import TypedDict


class ProductData(TypedDict):
    """Структура данных о товаре."""
    quantity: int
    price: float
    category: str


# Константы для валидации
MIN_QUANTITY: int = 0
MIN_PRICE: float = 0.0

# Сообщения об ошибках
ERROR_PRODUCT_EXISTS: str = "Товар '{name}' уже существует."
ERROR_PRODUCT_NOT_FOUND: str = "Товар '{name}' не найден."
ERROR_INVALID_QUANTITY: str = "Ошибка: количество должно быть целым неотрицательным числом."
ERROR_INVALID_PRICE: str = "Ошибка: цена должна быть неотрицательным числом."
ERROR_INVALID_DELTA: str = "Ошибка: изменение должно быть целым числом."
ERROR_NO_PRODUCTS: str = "Товары отсутствуют."
ERROR_NO_CATEGORIES: str = "Нет категорий."

# Сообщения меню
MENU_TITLE: str = "=== Система учета товаров ==="
MENU_OPTIONS: Dict[str, str] = {
    '1': 'Добавить товар',
    '2': 'Изменить количество',
    '3': 'Удалить товар',
    '4': 'Посчитать общую стоимость',
    '5': 'Найти самый дорогой товар',
    '6': 'Показать уникальные категории',
    '7': 'Выход',
}


class Inventory:
    """
    Класс для управления инвентарём товаров.

    Хранит информацию о товарах, их количестве, цене и категориях.
    """

    def __init__(self) -> None:
        """Инициализация пустого инвентаря."""
        self._products: Dict[str, ProductData] = {}
        self._categories: Set[str] = set()

    def add_product(
        self,
        name: str,
        quantity: int,
        price: float,
        category: str
    ) -> bool:
        """
        Добавление нового товара.

        Args:
            name: Название товара.
            quantity: Количество товара.
            price: Цена товара.
            category: Категория товара.

        Returns:
            True, если товар добавлен, False если уже существует.
        """
        if name in self._products:
            print(ERROR_PRODUCT_EXISTS.format(name=name))
            return False

        if quantity < MIN_QUANTITY:
            print(ERROR_INVALID_QUANTITY)
            return False

        if price < MIN_PRICE:
            print(ERROR_INVALID_PRICE)
            return False

        self._products[name] = {
            'quantity': quantity,
            'price': price,
            'category': category
        }
        self._categories.add(category)
        print(f"Добавлен товар '{name}'.")
        return True

    def change_quantity(self, name: str, delta: int) -> bool:
        """
        Изменение количества товара.

        Args:
            name: Название товара.
            delta: Изменение количества (может быть отрицательным).

        Returns:
            True, если количество изменено, False в случае ошибки.
        """
        if name not in self._products:
            print(ERROR_PRODUCT_NOT_FOUND.format(name=name))
            return False

        self._products[name]['quantity'] += delta
        print(
            f"Кол-во товара '{name}' изменено на {delta}. "
            f"Текущее кол-во: {self._products[name]['quantity']}"
        )
        return True

    def delete_product(self, name: str) -> bool:
        """
        Удаление товара из инвентаря.

        Args:
            name: Название товара для удаления.

        Returns:
            True, если товар удалён, False если не найден.
        """
        if name not in self._products:
            print(ERROR_PRODUCT_NOT_FOUND.format(name=name))
            return False

        category = self._products[name]['category']
        del self._products[name]

        # Удаляем категорию, если она больше не используется
        if not any(p['category'] == category for p in self._products.values()):
            self._categories.discard(category)

        print(f"Удалён товар '{name}'.")
        return True

    def calculate_total_value(self) -> float:
        """
        Вычисление общей стоимости всех товаров.

        Returns:
            Общая стоимость.
        """
        return sum(
            product['quantity'] * product['price']
            for product in self._products.values()
        )

    def print_total_value(self) -> float:
        """Вывод и возврат общей стоимости товаров."""
        total = self.calculate_total_value()
        print(f"Общая стоимость всех товаров: {total:.2f}")
        return total

    def get_most_expensive(self) -> Optional[Tuple[str, ProductData]]:
        """
        Поиск самого дорогого товара.

        Returns:
            Кортеж (название, данные) или None, если товаров нет.
        """
        if not self._products:
            return None
        return max(self._products.items(), key=lambda item: item[1]['price'])

    def print_most_expensive(self) -> Optional[Tuple[str, ProductData]]:
        """Вывод и возврат самого дорогого товара."""
        result = self.get_most_expensive()
        if result is None:
            print(ERROR_NO_PRODUCTS)
            return None

        name, data = result
        print(f"Самый дорогой товар: {name} по цене {data['price']:.2f}")
        return result

    def get_categories(self) -> Set[str]:
        """
        Получение множества уникальных категорий.

        Returns:
            Множество категорий.
        """
        return self._categories.copy()

    def print_categories(self) -> None:
        """Вывод уникальных категорий товаров."""
        if not self._categories:
            print(ERROR_NO_CATEGORIES)
            return

        print("Уникальные категории товаров:")
        for category in sorted(self._categories):
            print(f"- {category}")


def get_int_input(prompt: str, allow_negative: bool = False) -> Optional[int]:
    """
    Безопасный ввод целого числа.

    Args:
        prompt: Текст приглашения для ввода.
        allow_negative: Разрешить ли отрицательные числа.

    Returns:
        Введённое число или None, если ввод некорректен.
    """
    try:
        value = int(input(prompt).strip())
        if not allow_negative and value < 0:
            print(ERROR_INVALID_QUANTITY)
            return None
        return value
    except ValueError:
        print(ERROR_INVALID_DELTA)
        return None
    except KeyboardInterrupt:
        print("\nВвод прерван пользователем.")
        return None


def get_float_input(prompt: str) -> Optional[float]:
    """
    Безопасный ввод вещественного числа.

    Args:
        prompt: Текст приглашения для ввода.

    Returns:
        Введённое число или None, если ввод некорректен.
    """
    try:
        value = float(input(prompt).strip())
        if value < 0:
            print(ERROR_INVALID_PRICE)
            return None
        return value
    except ValueError:
        print(ERROR_INVALID_PRICE)
        return None
    except KeyboardInterrupt:
        print("\nВвод прерван пользователем.")
        return None


def print_menu() -> None:
    """Вывод меню программы."""
    print(f"\n{MENU_TITLE}")
    for key, value in MENU_OPTIONS.items():
        print(f"{key}. {value}")


def inventory_system() -> None:
    """
    Консольный интерфейс системы инвентаря.

    Запускает интерактивный цикл для управления товарами.
    """
    inv = Inventory()

    while True:
        print_menu()
        try:
            choice = input("Выберите действие: ").strip()
        except KeyboardInterrupt:
            print("\nРабота программы прервана.")
            break

        if choice == '1':
            name = input("Введите название товара: ").strip()
            quantity = get_int_input("Введите количество: ")
            price = get_float_input("Введите цену: ")
            category = input("Введите категорию: ").strip()
            if name and quantity is not None and price is not None and category:
                inv.add_product(name, quantity, price, category)

        elif choice == '2':
            name = input("Введите название товара: ").strip()
            delta = get_int_input(
                "Введите изменение количества (можно отрицательное): ",
                allow_negative=True
            )
            if name and delta is not None:
                inv.change_quantity(name, delta)

        elif choice == '3':
            name = input("Введите название товара: ").strip()
            if name:
                inv.delete_product(name)

        elif choice == '4':
            inv.print_total_value()

        elif choice == '5':
            inv.print_most_expensive()

        elif choice == '6':
            inv.print_categories()

        elif choice == '7':
            break

        else:
            print("Неверный выбор.")


def main() -> None:
    """Точка входа программы."""
    inventory_system()


if __name__ == "__main__":
    main()

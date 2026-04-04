#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Лабораторная работа №5: Продвинутые возможности Python
Темы: исключения, итераторы, генераторы, декораторы, контекстные менеджеры
"""

import time
import os
from functools import wraps
from contextlib import contextmanager
from typing import Any


# =============================================================================
# Задание 1.1: Иерархия исключений для банковской системы
# =============================================================================

class BankError(Exception):
    """Базовое исключение для банковской системы"""
    pass


class AccountNotFoundError(BankError):
    """Счёт не найден"""
    
    def __init__(self, account_id: str):
        self.account_id = account_id
        super().__init__(f"Счёт с ID {account_id} не найден")


class InsufficientFundsError(BankError):
    """Недостаточно средств на счёте"""
    
    def __init__(self, account_id: str, required: float, available: float):
        self.account_id = account_id
        self.required = required
        self.available = available
        super().__init__(
            f"Недостаточно средств на счёте {account_id}: "
            f"требуется {required}, доступно {available}"
        )


class InvalidAmountError(BankError):
    """Некорректная сумма"""
    
    def __init__(self, amount: float, reason: str = ""):
        self.amount = amount
        self.reason = reason
        message = f"Некорректная сумма: {amount}"
        if reason:
            message += f" ({reason})"
        super().__init__(message)


class BankAccount:
    """Класс банковского счёта"""
    
    def __init__(self, account_id: str, owner: str, initial_balance: float = 0.0):
        self.account_id = account_id
        self.owner = owner
        self._balance = initial_balance
    
    @property
    def balance(self) -> float:
        return self._balance
    
    def deposit(self, amount: float) -> None:
        """Внести деньги на счёт"""
        if amount <= 0:
            raise InvalidAmountError(amount, "сумма должна быть положительной")
        self._balance += amount
    
    def withdraw(self, amount: float) -> None:
        """Снять деньги со счёта"""
        if amount <= 0:
            raise InvalidAmountError(amount, "сумма должна быть положительной")
        if amount > self._balance:
            raise InsufficientFundsError(self.account_id, amount, self._balance)
        self._balance -= amount
    
    def transfer_to(self, target: "BankAccount", amount: float) -> None:
        """Перевод денег на другой счёт"""
        self.withdraw(amount)
        try:
            target.deposit(amount)
        except Exception:
            # Откат транзакции при ошибке
            self._balance += amount
            raise


def transfer_money(
    source: BankAccount,
    target: BankAccount,
    amount: float
) -> bool:
    """
    Перевод денег между счетами с обработкой исключений
    
    :param source: Счёт отправителя
    :param target: Счёт получателя
    :param amount: Сумма перевода
    :return: True если перевод успешен
    """
    try:
        source.transfer_to(target, amount)
        return True
    except (AccountNotFoundError, InsufficientFundsError, InvalidAmountError) as e:
        print(f"Ошибка перевода: {e}")
        return False


# =============================================================================
# Задание 2.1: Класс-итератор Cycle (циклический перебор элементов)
# =============================================================================

class Cycle:
    """Итератор, циклически возвращающий элементы списка"""
    
    def __init__(self, items: list):
        if not items:
            raise ValueError("Список не должен быть пустым")
        self.items = items
        self.index = 0
    
    def __iter__(self) -> "Cycle":
        return self
    
    def __next__(self) -> Any:
        if not self.items:
            raise StopIteration
        item = self.items[self.index]
        self.index = (self.index + 1) % len(self.items)
        return item


# =============================================================================
# Задание 3.1: Генератор для чтения файла построчно
# =============================================================================

def read_large_file(filename: str):
    """
    Генератор, читающий файл построчно
    
    :param filename: Имя файла для чтения
    :yield: Строки файла без пробельных символов по краям
    """
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped:  # Пропускаем пустые строки
                yield stripped


# =============================================================================
# Задание 4.1: Декоратор log_calls для логирования вызовов функций
# =============================================================================

def log_calls(filename: str = "log.txt"):
    """
    Декоратор, записывающий в файл информацию о вызовах функции
    
    :param filename: Имя файла для логирования
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            log_entry = (
                f"[{timestamp}] Вызов функции: {func.__name__}\n"
                f"  Аргументы: args={args}, kwargs={kwargs}\n"
            )
            with open(filename, "a", encoding="utf-8") as f:
                f.write(log_entry)
            return func(*args, **kwargs)
        return wrapper
    return decorator


# =============================================================================
# Задание 5.1: Контекстный менеджер Timer (два способа реализации)
# =============================================================================

class Timer:
    """Контекстный менеджер для замера времени выполнения блока кода (класс)"""
    
    def __init__(self, description: str = "Блок кода"):
        self.description = description
        self.start_time: float = 0.0
        self.end_time: float = 0.0
    
    def __enter__(self) -> "Timer":
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.end_time = time.time()
        elapsed = self.end_time - self.start_time
        print(f"{self.description} выполнился за {elapsed:.4f} сек")
        return False


@contextmanager
def timer_context(description: str = "Блок кода"):
    """Контекстный менеджер для замера времени (через @contextmanager)"""
    start_time = time.time()
    try:
        yield
    finally:
        end_time = time.time()
        elapsed = end_time - start_time
        print(f"{description} выполнился за {elapsed:.4f} сек")


# =============================================================================
# Задание 6.1: Декоратор @cache для кэширования результатов функций
# =============================================================================

def cache(func):
    """
    Декоратор для кэширования результатов вызова функции
    
    :param func: Функция для кэширования
    :return: Обёртка с кэшированием
    """
    cache_dict: dict[tuple, Any] = {}
    
    @wraps(func)
    def wrapper(*args):
        if args not in cache_dict:
            cache_dict[args] = func(*args)
        return cache_dict[args]
    
    wrapper.cache_info = lambda: len(cache_dict)  # type: ignore[attr-defined]
    wrapper.cache_clear = lambda: cache_dict.clear()  # type: ignore[attr-defined]
    return wrapper


def fibonacci(n: int) -> int:
    """Рекурсивное вычисление чисел Фибоначчи (без кэша)"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@cache
def fibonacci_cached(n: int) -> int:
    """Рекурсивное вычисление чисел Фибоначчи с кэшированием"""
    if n <= 1:
        return n
    return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)


# =============================================================================
# Демонстрация работы
# =============================================================================

def demo_banking():
    """Демонстрация банковской системы с исключениями"""
    print("\n=== Задание 1.1: Банковская система ===")
    
    account1 = BankAccount("ACC001", "Иван Иванов", 1000.0)
    account2 = BankAccount("ACC002", "Пётр Петров", 500.0)
    
    print(f"Счёт 1: {account1.balance} руб.")
    print(f"Счёт 2: {account2.balance} руб.")
    
    # Успешный перевод
    print("\nПеревод 200 руб. со счёта 1 на счёт 2...")
    success = transfer_money(account1, account2, 200.0)
    print(f"Перевод успешен: {success}")
    print(f"Счёт 1: {account1.balance} руб.")
    print(f"Счёт 2: {account2.balance} руб.")
    
    # Попытка перевода большей суммы
    print("\nПопытка перевода 5000 руб...")
    success = transfer_money(account1, account2, 5000.0)
    print(f"Перевод успешен: {success}")
    
    # Некорректная сумма
    print("\nПопытка перевода отрицательной суммы...")
    success = transfer_money(account1, account2, -100.0)
    print(f"Перевод успешен: {success}")


def demo_cycle():
    """Демонстрация итератора Cycle"""
    print("\n=== Задание 2.1: Итератор Cycle ===")
    
    cycle = Cycle(["A", "B", "C"])
    print("Первые 10 элементов циклического итератора ['A', 'B', 'C']:")
    for i, item in enumerate(cycle):
        if i >= 10:
            break
        print(item, end=" ")
    print()


def demo_generator():
    """Демонстрация генератора read_large_file"""
    print("\n=== Задание 3.1: Генератор read_large_file ===")
    
    # Создаём тестовый файл
    test_file = "data/test_read_large_file.txt"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("Строка 1\n")
        f.write("\n")  # Пустая строка
        f.write("  Строка 2 с пробелами  \n")
        f.write("Строка 3\n")
        f.write("\n")
        f.write("Строка 4\n")
    
    print(f"Чтение файла {test_file} построчно:")
    for i, line in enumerate(read_large_file(test_file), 1):
        print(f"  {i}: '{line}'")
    
    # Удаляем тестовый файл
    os.remove(test_file)


@log_calls("data/log.txt")
def add(a: int, b: int) -> int:
    """Сложение двух чисел"""
    return a + b


@log_calls("data/log.txt")
def multiply(a: int, b: int) -> int:
    """Умножение двух чисел"""
    return a * b


def demo_decorator():
    """Демонстрация декоратора log_calls"""
    print("\n=== Задание 4.1: Декоратор log_calls ===")
    
    # Очищаем лог-файл
    log_file = "data/log.txt"
    if os.path.exists(log_file):
        os.remove(log_file)
    
    print("Вызов функций с логированием...")
    result1 = add(5, 3)
    result2 = multiply(4, 7)
    
    print(f"add(5, 3) = {result1}")
    print(f"multiply(4, 7) = {result2}")
    
    # Читаем лог-файл
    with open(log_file, "r", encoding="utf-8") as f:
        log_content = f.read()
    
    print(f"\nСодержимое {log_file}:")
    print(log_content)


def demo_timer():
    """Демонстрация контекстного менеджера Timer"""
    print("\n=== Задание 5.1: Контекстный менеджер Timer ===")
    
    print("\nТаймер через класс:")
    with Timer("Сон 0.5 сек") as t:
        time.sleep(0.5)
    
    print("\nТаймер через @contextmanager:")
    with timer_context("Сон 0.3 сек"):
        time.sleep(0.3)


def demo_cache():
    """Демонстрация декоратора @cache"""
    print("\n=== Задание 6.1: Декоратор @cache ===")
    
    # Без кэша (медленно)
    print("\nВычисление fibonacci(30) без кэша...")
    start = time.time()
    result_no_cache = fibonacci(30)
    time_no_cache = time.time() - start
    print(f"  Результат: {result_no_cache}")
    print(f"  Время: {time_no_cache:.4f} сек")
    
    # С кэшем (быстро)
    print("\nВычисление fibonacci_cached(30) с кэшем...")
    start = time.time()
    result_cache = fibonacci_cached(30)
    time_cache = time.time() - start
    print(f"  Результат: {result_cache}")
    print(f"  Время: {time_cache:.4f} сек")
    
    print(f"\nУскорение: {time_no_cache / time_cache:.2f}x")
    print(f"Размер кэша: {fibonacci_cached.cache_info()} записей")  # type: ignore[attr-defined]


def main():
    """Основная функция для демонстрации всех заданий"""
    print("Лабораторная работа №5: Продвинутые возможности Python")
    print("=" * 60)
    
    demo_banking()
    demo_cycle()
    demo_generator()
    demo_decorator()
    demo_timer()
    demo_cache()
    
    print("\n" + "=" * 60)
    print("Все задания выполнены успешно!")


if __name__ == "__main__":
    main()

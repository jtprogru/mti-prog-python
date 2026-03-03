#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Утилита для запуска лабораторных работ.

Использование:
    python run.py              # Показать список доступных скриптов
    python run.py lab1         # Запустить конкретный скрипт
    python run.py calculator   # Запустить калькулятор
"""

import sys
import os
from pathlib import Path

# Добавляем корень проекта в PATH
PROJECT_ROOT = Path(__file__).resolve().parent
LABS_DIR = PROJECT_ROOT / "labs"

# Список доступных лабораторных работ (без __init__.py)
AVAILABLE_LABS = [
    f.stem for f in LABS_DIR.glob("*.py")
    if f.name != "__init__.py" and f.is_file()
]


def print_usage():
    """Выводит справку по использованию."""
    print("\n=== Лабораторные работы по Python ===\n")
    print("Доступные скрипты:")
    for lab in sorted(AVAILABLE_LABS):
        print(f"  - {lab}")
    print("\nИспользование:")
    print("  python run.py <имя_скрипта>   Запустить указанный скрипт")
    print("  python run.py                 Показать эту справку\n")
    print("Примеры:")
    print("  python run.py lab1")
    print("  python run.py calculator")
    print("  python run.py diary_app")


def run_lab(lab_name: str):
    """Запускает указанную лабораторную работу."""
    lab_file = LABS_DIR / f"{lab_name}.py"
    
    if not lab_file.exists():
        print(f"Ошибка: Скрипт '{lab_name}.py' не найден.")
        print(f"Доступные скрипты: {', '.join(sorted(AVAILABLE_LABS))}")
        return False
    
    # Добавляем labs в sys.path для импорта
    sys.path.insert(0, str(LABS_DIR))
    
    # Импортируем и запускаем main()
    try:
        module = __import__(lab_name)
        if hasattr(module, "main"):
            module.main()
        else:
            print(f"Ошибка: В скрипте '{lab_name}.py' нет функции main()")
            return False
    except Exception as e:
        print(f"Ошибка при выполнении скрипта: {e}")
        return False
    
    return True


def main():
    if len(sys.argv) < 2:
        print_usage()
        return
    
    lab_name = sys.argv[1]
    
    if lab_name in ("-h", "--help", "help"):
        print_usage()
        return
    
    run_lab(lab_name)


if __name__ == "__main__":
    main()

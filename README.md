# Лабораторные работы по программированию на Python

Этот репозиторий содержит небольшие самостоятельные скрипты, демонстрирующие базовые возможности Python. Каждый скрипт имеет функцию `main()` и может запускаться непосредственно.

## Структура проекта

```
mti-prog-python/
├── labs/           # Лабораторные работы (скрипты)
├── utils/          # Вспомогательные утилиты
├── data/           # Данные (JSON-файлы для скриптов)
├── run.py          # Утилита для запуска скриптов
└── pyproject.toml  # Конфигурация проекта
```

## Как запустить

### Вариант 1: Через uv (рекомендуется)

```bash
# Синхронизировать окружение и установить зависимости
uv sync

# Запустить скрипт через uv run
uv run labs lab1
uv run labs calculator

# Или напрямую через entry point
uv run labs
```

### Вариант 2: Через утилиту run.py

```bash
# Показать список доступных скриптов
python run.py

# Запустить конкретный скрипт
python run.py lab1
python run.py calculator
```

### Вариант 3: Прямой запуск

```bash
python labs/<скрипт>.py

# Примеры:
python labs/lab1.py
python labs/calculator.py
python labs/diary_app.py
```

### Виртуальное окружение

#### Через uv (рекомендуется)

```bash
# Создание и активация
uv venv
source .venv/bin/activate

# Запуск скрипта
python run.py lab1

# Деактивация
deactivate
```

#### Через Python (опционально)

```bash
# Создание
python -m venv .venv

# Активация (macOS/Linux)
source .venv/bin/activate

# Запуск скрипта
python run.py lab1

# Деактивация
deactivate
```

## Список скриптов

| Скрипт | Что делает | Как запустить |
|--------|------------|----------------|
| `lab1` | Приветствие, демонстрация базовых типов и операций | `python run.py lab1` |
| `calculator` | Простой калькулятор с арифметикой | `python run.py calculator` |
| `anketa` | Сбор анкеты пользователя и вывод таблицы | `python run.py anketa` |
| `triangle` | Вычисление площади и периметра треугольника | `python run.py triangle` |
| `multiplication_table` | Вывод таблицы умножения | `python run.py multiplication_table` |
| `sentence_analysis` | Анализ предложения (слова, символы) | `python run.py sentence_analysis` |
| `student_grades` | Учёт оценок студентов | `python run.py student_grades` |
| `inventory` | Пример работы с инвентарём | `python run.py inventory` |
| `library_system` | Симуляция библиотеки (книги, читатели) | `python run.py library_system` |
| `main_lab3` | Дополнительный пример | `python run.py main_lab3` |
| `string_operations` | Операции со строками | `python run.py string_operations` |
| `diary_app` | Простейшее приложение‑дневник | `python run.py diary_app` |

## Требования

- Python 3.14 или выше
- Внешние зависимости не требуются (используется только стандартная библиотека)

## Данные

Скрипты `diary_app` и `library_system` сохраняют данные в JSON-файлы в директории `data/`:
- `data/tasks.json` — задачи ежедневника
- `data/library_data.json` — данные библиотеки

## Расширение проекта

### Добавление новой лабораторной работы

1. Создайте файл `labs/<имя>.py` в корне репозитория
2. Добавьте shebang и кодировку:
   ```python
   #!/usr/bin/env python3
   # -*- coding: utf-8 -*-
   ```
3. Реализуйте функцию `main()` с логикой
4. Добавьте блок `if __name__ == "__main__": main()`
5. Обновите этот README, добавив скрипт в таблицу

### Стиль кода

- Имена переменных: `snake_case`
- Кодировка: UTF-8
- Обработка ошибок: `try/except` с валидацией ввода
- Интерактивность: `input()` для взаимодействия с пользователем

## Управление зависимостями через uv

Проект использует [`uv`](https://docs.astral.sh/uv/) для управления зависимостями и виртуальным окружением.

### Основные команды

```bash
# Установка зависимостей и создание окружения
uv sync

# Запуск скрипта без активации окружения
uv run labs lab1

# Добавление новой зависимости
uv add <пакет>

# Добавление dev-зависимости (линтеры, тесты)
uv add --dev <пакет>

# Запуск dev-инструментов
uv run ruff check labs/
uv run mypy labs/
```

### Установка uv

Если `uv` ещё не установлен:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Или через pip
pip install uv

# Или через Homebrew
brew install uv
```

## Примечание

Все скрипты независимы и не используют общую базу данных. При желании можете добавить свои упражнения, следуя тем же конвенциям.

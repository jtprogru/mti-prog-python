# multiplication_table.py
def multiplication_table():
    print("=== Таблица умножения ===")
    try:
        n = int(input("Введите N (верхняя граница таблицы): "))
    except ValueError:
        print("Ошибка: введено не целое число.")
        return
    if n <= 0:
        print("N должно быть положительным.")
        return

    max_val = n * n
    width = len(str(max_val)) + 1

    header = "    "
    for col in range(1, n + 1):
        header += f"{col:>{width}}"
    print(header)

    for row in range(1, n + 1):
        line = f"{row:>3} "
        for col in range(1, n + 1):
            line += f"{row * col:>{width}}"
        print(line)


if __name__ == "__main__":
    multiplication_table()

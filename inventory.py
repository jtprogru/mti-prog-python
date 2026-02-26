# inventory.py
class Inventory:
    def __init__(self):
        self.products = {}  # name -> dict(quantity, price, category)
        self.categories = set()

    def add_product(self, name, quantity, price, category):
        if name in self.products:
            print(f"Товар '{name}' уже существует.")
            return
        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            print("Ошибка: количество должно быть целым, цена — числом.")
            return
        self.products[name] = {
            'quantity': quantity,
            'price': price,
            'category': category
        }
        self.categories.add(category)
        print(f"Добавлен товар '{name}'.")

    def change_quantity(self, name, delta):
        if name not in self.products:
            print(f"Товар '{name}' не найден.")
            return
        try:
            delta = int(delta)
        except ValueError:
            print("Ошибка: изменение должно быть целым числом.")
            return
        self.products[name]['quantity'] += delta
        print(f"Кол-во товара '{name}' изменено на {delta}. Текущее кол-во: {self.products[name]['quantity']}")

    def delete_product(self, name):
        if name in self.products:
            category = self.products[name]['category']
            del self.products[name]
            if not any(p['category'] == category for p in self.products.values()):
                self.categories.discard(category)
            print(f"Удалён товар '{name}'.")
        else:
            print(f"Товар '{name}' не найден.")

    def total_value(self):
        total = sum(p['quantity'] * p['price'] for p in self.products.values())
        print(f"Общая стоимость всех товаров: {total:.2f}")
        return total

    def most_expensive(self):
        if not self.products:
            print("Товары отсутствуют.")
            return None
        name, data = max(self.products.items(), key=lambda item: item[1]['price'])
        print(f"Самый дорогой товар: {name} по цене {data['price']:.2f}")
        return name, data

    def print_categories(self):
        if not self.categories:
            print("Нет категорий.")
            return
        print("Уникальные категории товаров:")
        for cat in sorted(self.categories):
            print(f"- {cat}")


def inventory_system():
    inv = Inventory()
    while True:
        print("\n=== Система учета товаров ===")
        print("1. Добавить товар")
        print("2. Изменить количество")
        print("3. Удалить товар")
        print("4. Посчитать общую стоимость")
        print("5. Найти самый дорогой товар")
        print("6. Показать уникальные категории")
        print("7. Выход")
        choice = input("Выберите действие: ").strip()
        if choice == '1':
            name = input("Введите название товара: ").strip()
            quantity = input("Введите количество: ").strip()
            price = input("Введите цену: ").strip()
            category = input("Введите категорию: ").strip()
            inv.add_product(name, quantity, price, category)
        elif choice == '2':
            name = input("Введите название товара: ").strip()
            delta = input("Введите изменение количества (можно отрицательное): ").strip()
            inv.change_quantity(name, delta)
        elif choice == '3':
            name = input("Введите название товара: ").strip()
            inv.delete_product(name)
        elif choice == '4':
            inv.total_value()
        elif choice == '5':
            inv.most_expensive()
        elif choice == '6':
            inv.print_categories()
        elif choice == '7':
            break
        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    inventory_system()

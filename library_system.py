# library_system.py
import json
from datetime import datetime, timedelta

class LibrarySystem:
    def __init__(self):
        self.books = {}  # {id: {title, author, year, status, due_date}}
        self.readers = {}  # {reader_id: {name, ticket, borrowed_books}}
        self.next_book_id = 1
        self.next_reader_id = 1
        self.fine_per_day = 0.5  # штраф за просрочку в день

    def add_book(self, title, author, year):
        book_id = self.next_book_id
        self.books[book_id] = {
            'title': title,
            'author': author,
            'year': year,
            'status': 'available',
            'due_date': None
        }
        self.next_book_id += 1
        print(f"Книга '{title}' добавлена с ID {book_id}")

    def register_reader(self, name):
        reader_id = self.next_reader_id
        self.readers[reader_id] = {
            'name': name,
            'ticket': f"T{reader_id:03d}",
            'borrowed_books': []
        }
        self.next_reader_id += 1
        print(f"Читатель '{name}' зарегистрирован с ID {reader_id}")

    def borrow_book(self, reader_id, book_id):
        if reader_id not in self.readers:
            print("Читатель не найден!")
            return

        if book_id not in self.books:
            print("Книга не найдена!")
            return

        if self.books[book_id]['status'] != 'available':
            print("Книга уже выдана!")
            return

        due_date = datetime.now() + timedelta(days=14)
        self.books[book_id]['status'] = 'borrowed'
        self.books[book_id]['due_date'] = due_date.strftime("%Y-%m-%d")
        self.readers[reader_id]['borrowed_books'].append(book_id)

        print(f"Книга '{self.books[book_id]['title']}' выдана читателю '{self.readers[reader_id]['name']}' до {due_date.strftime('%d.%m.%Y')}")

    def return_book(self, reader_id, book_id):
        if reader_id not in self.readers:
            print("Читатель не найден!")
            return

        if book_id not in self.books:
            print("Книга не найдена!")
            return

        if book_id not in self.readers[reader_id]['borrowed_books']:
            print("Эта книга не была выдана данному читателю!")
            return

        # Проверка просрочки
        today = datetime.now().date()
        due_date_str = self.books[book_id]['due_date']
        if due_date_str:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
            if today > due_date:
                days_overdue = (today - due_date).days
                fine = days_overdue * self.fine_per_day
                print(f"Книга просрочена на {days_overdue} дней. Штраф: ${fine:.2f}")
            else:
                print("Книга возвращена вовремя.")
        else:
            print("Дата возврата не определена, это ошибка.")

        self.books[book_id]['status'] = 'available'
        self.books[book_id]['due_date'] = None
        self.readers[reader_id]['borrowed_books'].remove(book_id)

        print(f"Книга '{self.books[book_id]['title']}' возвращена.")

    def search_books(self, keyword):
        print(f"\nРезультаты поиска по '{keyword}':")
        found = False
        for book_id, book in self.books.items():
            if (keyword.lower() in book['title'].lower() or
                    keyword.lower() in book['author'].lower()):
                status = "✓ доступна" if book['status'] == 'available' else f"✗ выдана до {book['due_date']}"
                print(f"ID: {book_id}, '{book['title']}', {book['author']}, {book['year']} - {status}")
                found = True
        if not found:
            print("Книги не найдены")

    def show_all_books(self):
        print("\n=== Все книги в библиотеке ===")
        for book_id, book in self.books.items():
            status = "✓ доступна" if book['status'] == 'available' else f"✗ выдана до {book['due_date']}"
            print(f"ID: {book_id}, '{book['title']}', {book['author']}, {book['year']} - {status}")

    def show_all_readers(self):
        print("\n=== Все читатели ===")
        for reader_id, reader in self.readers.items():
            print(f"\nID: {reader_id}, {reader['name']}, Билет: {reader['ticket']}")
            if reader['borrowed_books']:
                print("Взятые книги:")
                for book_id in reader['borrowed_books']:
                    print(f" - {self.books[book_id]['title']}")
            else:
                print("Нет взятых книг")

    def check_overdue(self):
        today = datetime.now().date()
        overdue_info = []
        for book_id, book in self.books.items():
            if book['status'] == 'borrowed':
                due_date = datetime.strptime(book['due_date'], "%Y-%m-%d").date()
                if today > due_date:
                    days_overdue = (today - due_date).days
                    overdue_info.append((book_id, book['title'], days_overdue))
        if overdue_info:
            print("\nПросроченные книги:")
            for bid, title, days in overdue_info:
                print(f"ID {bid}: '{title}' просрочено на {days} дней.")
        else:
            print("\nНи одна книга не просрочена.")

    def save_to_file(self, filename='library_data.json'):
        data = {
            'books': self.books,
            'readers': self.readers,
            'next_book_id': self.next_book_id,
            'next_reader_id': self.next_reader_id
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Данные сохранены в {filename}")

    def load_from_file(self, filename='library_data.json'):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.books = data.get('books', {})
            self.readers = data.get('readers', {})
            self.next_book_id = data.get('next_book_id', 1)
            self.next_reader_id = data.get('next_reader_id', 1)
            print(f"Данные загружены из {filename}")
        except FileNotFoundError:
            print(f"Файл {filename} не найден.")


def library_system():
    lib = LibrarySystem()
    lib.load_from_file()

    while True:
        print("\n=== Система управления библиотекой ===")
        print("1. Добавить книгу")
        print("2. Зарегистрировать читателя")
        print("3. Выдать книгу")
        print("4. Вернуть книгу")
        print("5. Поиск книг")
        print("6. Показать все книги")
        print("7. Показать всех читателей")
        print("8. Проверить просроченные книги")
        print("9. Сохранить данные")
        print("10. Завершить")
        choice = input("Выберите действие: ").strip()
        if choice == '1':
            title = input("Введите название книги: ").strip()
            author = input("Введите автора: ").strip()
            year = input("Введите год публикации: ").strip()
            lib.add_book(title, author, year)
        elif choice == '2':
            name = input("Введите ФИО читателя: ").strip()
            lib.register_reader(name)
        elif choice == '3':
            try:
                reader_id = int(input("Введите ID читателя: "))
                book_id = int(input("Введите ID книги: "))
                lib.borrow_book(reader_id, book_id)
            except ValueError:
                print("Ошибка: ID должно быть числом.")
        elif choice == '4':
            try:
                reader_id = int(input("Введите ID читателя: "))
                book_id = int(input("Введите ID книги: "))
                lib.return_book(reader_id, book_id)
            except ValueError:
                print("Ошибка: ID должно быть числом.")
        elif choice == '5':
            keyword = input("Введите ключевое слово: ").strip()
            lib.search_books(keyword)
        elif choice == '6':
            lib.show_all_books()
        elif choice == '7':
            lib.show_all_readers()
        elif choice == '8':
            lib.check_overdue()
        elif choice == '9':
            lib.save_to_file()
        elif choice == '10':
            lib.save_to_file()
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор.")


def main():
    library_system()


if __name__ == "__main__":
    main()

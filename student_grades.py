# student_grades.py
class StudentGrades:
    def __init__(self):
        self.grades = {}  # name -> list of grades

    def add_student(self, name):
        if name in self.grades:
            print(f"Студент {name} уже существует.")
        else:
            self.grades[name] = []
            print(f"Добавлен студент {name}.")

    def add_grade(self, name, grade):
        if name not in self.grades:
            print(f"Студент {name} не найден.")
            return
        try:
            grade = float(grade)
        except ValueError:
            print("Ошибка: оценка должна быть числом.")
            return
        self.grades[name].append(grade)
        print(f"Добавлена оценка {grade} для {name}.")

    def delete_student(self, name):
        if name in self.grades:
            del self.grades[name]
            print(f"Удалён студент {name}.")
        else:
            print(f"Студент {name} не найден.")

    def average_grade(self, name):
        if name not in self.grades or not self.grades[name]:
            print(f"Нет оценок для {name}.")
            return None
        avg = sum(self.grades[name]) / len(self.grades[name])
        print(f"Средняя оценка для {name}: {avg:.2f}")
        return avg

    def print_all_averages(self):
        print("Список студентов и их средние баллы:")
        for name, grades in self.grades.items():
            if grades:
                avg = sum(grades) / len(grades)
                print(f"{name}: {avg:.2f}")
            else:
                print(f"{name}: нет оценок")

    def top_student(self):
        best_name = None
        best_avg = -1
        for name, grades in self.grades.items():
            if grades:
                avg = sum(grades) / len(grades)
                if avg > best_avg:
                    best_avg = avg
                    best_name = name
        if best_name:
            print(f"Лучший студент: {best_name} со средним баллом {best_avg:.2f}")
        else:
            print("Нет студентов с оценками.")


def student_grades_system():
    system = StudentGrades()
    while True:
        print("\n=== Система оценок студентов ===")
        print("1. Добавить студента")
        print("2. Добавить оценку")
        print("3. Удалить студента")
        print("4. Показать средний балл студента")
        print("5. Показать всех студентов со средними баллами")
        print("6. Найти студента с самым высоким средним баллом")
        print("7. Выход")
        choice = input("Выберите действие: ").strip()
        if choice == '1':
            name = input("Введите имя студента: ").strip()
            system.add_student(name)
        elif choice == '2':
            name = input("Введите имя студента: ").strip()
            grade = input("Введите оценку: ").strip()
            system.add_grade(name, grade)
        elif choice == '3':
            name = input("Введите имя студента: ").strip()
            system.delete_student(name)
        elif choice == '4':
            name = input("Введите имя студента: ").strip()
            system.average_grade(name)
        elif choice == '5':
            system.print_all_averages()
        elif choice == '6':
            system.top_student()
        elif choice == '7':
            break
        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    student_grades_system()

# sentence_analysis.py
import re
from collections import Counter

def sentence_analysis():
    print("=== Анализ предложения ===")
    sentence = input("Введите предложение: ").strip()
    if not sentence:
        print("Пустая строка.")
        return

    words = re.findall(r'\b\w+\b', sentence, re.UNICODE)
    if not words:
        print("В предложении нет слов.")
        return

    longest = max(words, key=len)
    print(f"Самое длинное слово: {longest}")

    letters = [c.lower() for c in sentence if c.isalpha()]
    counter = Counter(letters)
    print("\nЧастота букв:")
    for letter, count in sorted(counter.items()):
        print(f"{letter}: {count}")


if __name__ == "__main__":
    sentence_analysis()

'''# =========================
# Частина 1: Легкі завдання
# =========================

# 1.1 Генерація паролів
import random
import string

def generate_password():
    upper = random.choice(string.ascii_uppercase)
    lower = random.choice(string.ascii_lowercase)
    digit = random.choice(string.digits)
    others = [random.choice(string.ascii_letters + string.digits) for _ in range(5)]
    password_list = [upper, lower, digit] + others
    random.shuffle(password_list)
    return ''.join(password_list)

for i in range(5):
    print(f"{i+1}. {generate_password()}")

# 1.2 Геометрія
import math

def circle_metrics(r):
    area = round(math.pi * r**2, 2)
    circumference = round(2 * math.pi * r, 2)
    return (area, circumference)

# 1.3 Дата народження
from datetime import datetime, date

def birthday_info(year, month, day):
    today = date.today()
    birth = date(year, month, day)

    age = today.year - birth.year - ((today.month, today.day) < (month, day))
    weekday = birth.strftime("%A")

    next_birthday = date(today.year, month, day)
    if next_birthday < today:
        next_birthday = date(today.year + 1, month, day)

    days_left = (next_birthday - today).days

    return age, weekday, days_left

# 1.4 Кубик
def dice_stats():
    rolls = [random.randint(1, 6) for _ in range(1000)]
    for i in range(1, 7):
        percent = rolls.count(i) / 1000 * 100
        print(f"Грань {i}: {percent:.1f}%")

# 1.5 Підрахунок рядків і слів
def file_stats(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    words = sum(len(line.split()) for line in lines)
    print(f"Рядків: {len(lines)}")
    print(f"Слів: {words}")

# 1.6 Найдовше слово
import string as st

def longest_word(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    for p in st.punctuation:
        text = text.replace(p, "")
    words = text.split()
    longest = max(words, key=len)
    print(f'Найдовше слово: "{longest}" ({len(longest)} символів)')

# 1.7 readline()
def sum_numbers(filename):
    total = 0
    with open(filename, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            total += float(line.strip())
    print("Сума чисел:", total)

# 1.8 Таблиця множення
def create_table():
    with open("multiplication_table.txt", "w", encoding="utf-8") as f:
        for i in range(1, 11):
            row = "\t".join([f"{i} × {j} = {i*j}" for j in range(1, 11)])
            f.write(row + "\n")

# 1.9 Щоденник
def add_diary_entry(text):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("diary.txt", "a", encoding="utf-8") as f:
        f.write(f"{now} - {text}\n")

# 1.10 Фільтрація рядків
def filter_file(src, dst):
    with open(src, 'r', encoding='utf-8') as f1, open(dst, 'w', encoding='utf-8') as f2:
        for line in f1:
            if len(line.strip()) > 20:
                f2.write(line)


# =========================
# Частина 2: Середні
# =========================

# 2.1 text_processor.py
def count_vowels(text):
    vowels = "aeiouAEIOUаеєиіїоуюяАЕЄИІЇОУЮЯ"
    return sum(1 for c in text if c in vowels)

def reverse_words(text):
    return " ".join(text.split()[::-1])

def to_pig_latin(text):
    return " ".join(word[1:] + word[0] + "ay" if len(word) > 1 else word for word in text.split())

# 2.2 calculator.py
class Calculator:
    def __init__(self):
        self.history = []

    def _log(self, expr, result):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"{now} | {expr} = {result}"
        self.history.append(entry)

    def add(self, a, b):
        res = a + b
        self._log(f"{a} + {b}", res)
        return res

    def subtract(self, a, b):
        res = a - b
        self._log(f"{a} - {b}", res)
        return res

    def multiply(self, a, b):
        res = a * b
        self._log(f"{a} * {b}", res)
        return res

    def divide(self, a, b):
        res = a / b
        self._log(f"{a} / {b}", res)
        return res

    def save(self, filename):
        with open(filename, 'w') as f:
            f.write("\n".join(self.history))

    def load(self, filename):
        with open(filename, 'r') as f:
            self.history = f.read().splitlines()

# 2.3 CSV аналіз
def analyze_grades(file):
    import csv
    students = []
    with open(file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            name, surname, *grades = row
            grades = list(map(int, grades))
            avg = sum(grades) / len(grades)
            students.append((name, surname, grades, avg))

    best = max(students, key=lambda x: x[3])

    subjects_avg = []
    for i in range(5):
        subjects_avg.append(round(sum(s[2][i] for s in students)/len(students), 1))

    with open("report.txt", "w", encoding="utf-8") as f:
        f.write("СЕРЕДНІ БАЛИ СТУДЕНТІВ:\n")
        for s in students:
            f.write(f"{s[0]} {s[1]}: {round(s[3],1)}\n")

        f.write(f"\nКРАЩИЙ СТУДЕНТ: {best[0]} {best[1]} ({round(best[3],1)})\n\n")

        f.write("СЕРЕДНІ БАЛИ З ПРЕДМЕТІВ:\n")
        for i, val in enumerate(subjects_avg, 1):
            f.write(f"Предмет {i}: {val}\n")

# 2.4 Менеджер паролів
def encrypt(text):
    return "".join(chr(ord(c)+1) for c in text)

def decrypt(text):
    return "".join(chr(ord(c)-1) for c in text)

def add_password(site, password, file="passwords.txt"):
    try:
        with open(file, "a") as f:
            f.write(f"{site}:{encrypt(password)}\n")
        print("Додано запис для", site)
    except Exception as e:
        print("Помилка:", e)

def get_password(site, file="passwords.txt"):
    try:
        with open(file) as f:
            for line in f:
                s, p = line.strip().split(":")
                if s == site:
                    print("Пароль:", decrypt(p))
    except FileNotFoundError:
        print("Файл не знайдено")

# 2.5 Об'єднання файлів
def merge_files(f1, f2, out):
    try:
        nums = set()
        for file in [f1, f2]:
            with open(file) as f:
                nums.update(int(line.strip()) for line in f)
        with open(out, "w") as f:
            for n in sorted(nums):
                f.write(str(n) + "\n")
    except Exception as e:
        print("Помилка:", e)


# =========================
# Частина 3: Складні
# =========================

# 3.1 Аналіз логів (спрощено)
def analyze_logs(file):
    from collections import Counter
    ips = Counter()
    pages = Counter()
    codes = Counter()

    with open(file) as f:
        for line in f:
            parts = line.split()
            ip = parts[0]
            page = parts[6]
            code = parts[8]

            ips[ip] += 1
            pages[page] += 1
            codes[code] += 1

    print("Популярна сторінка:", pages.most_common(1))
    print("Коди:", codes)

# 3.2 Інвентар (спрощено)
class Product:
    def __init__(self, name, category, price, qty):
        self.name = name
        self.category = category
        self.price = price
        self.qty = qty

class Inventory:
    def __init__(self):
        self.products = []

    def add(self, product):
        self.products.append(product)

    def sell(self, name, count):
        for p in self.products:
            if p.name == name:
                p.qty -= count

# 3.3 Аналіз студентів (каркас)
def analyze_students(data):
    avg = sum(sum(s[2:]) for s in data) / (len(data)*len(data[0][2:]))
    print("Середній бал:", avg)'''
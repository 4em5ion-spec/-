# =========================
# Частина 1: Легкі завдання
# =========================
'''
# 1.1
def say_hello():
    print("Вітаю! Ласкаво просимо до програми обчислень.")
'''
'''
# 1.2
def draw_frame():
    for i in range(5):
        if i == 0 or i == 4:
            print("*" * 20)
        else:
            print("*" + " " * 18 + "*")

''''''
# 1.3
from datetime import datetime

def show_datetime():
    now = datetime.now()
    print(f"Сьогодні: {now.strftime('%d.%m.%Y')}, час: {now.strftime('%H:%M')}")

''''''
# 1.4
def multiplication_table_7():
    for i in range(1, 11):
        print(f"7 × {i} = {7 * i}")

''''''
# 1.5
def calculate_age(birth_year):
    age = 2024 - birth_year
    if age % 10 == 1 and age != 11:
        word = "рік"
    elif 2 <= age % 10 <= 4 and not (12 <= age <= 14):
        word = "роки"
    else:
        word = "років"
    print(f"Ваш вік: {age} {word}")

''''''
# 1.6
def celsius_to_fahrenheit(celsius):
    f = celsius * 9/5 + 32
    print(f"{celsius}°C = {f:.1f}°F")

''''''
# 1.7
import random
import string

def generate_password(length):
    password = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
    print(password)

''''''
# 1.8
def triangle_area(base, height):
    return 0.5 * base * height
'''
'''
# 1.9
def is_even(number):
    return number % 2 == 0
'''
'''
# 1.10
def format_price(price):
    return f"Ціна: {price:.2f} грн."

'''
# =========================
# Частина 2: Середні
# =========================
'''
# 2.1
def calculate_discount(price, discount_percent, is_member=False):
    price -= price * (discount_percent / 100)
    if is_member:
        price -= price * 0.05
    return price
'''
'''
# 2.2
def format_address(city, street, house, apartment=None):
    address = f"м. {city}, вул. {street}, буд. {house}"
    if apartment:
        address += f", кв. {apartment}"
    return address
'''
'''
# 2.3
def text_statistics(text):
    chars = len(text)
    words = len(text.split()) if text else 0
    sentences = sum(text.count(c) for c in ".!?")
    return {
        'символів': chars,
        'слів': words,
        'речень': sentences
    }
'''
'''
# 2.4
def calculate_weight_cost(weight):
    if weight <= 5:
        return 50
    elif weight <= 10:
        return 80
    else:
        return 80 + (weight - 10) * 10


def calculate_delivery(distance, weight, is_express=False):
    weight_cost = calculate_weight_cost(weight)
    distance_cost = distance * (2 if is_express else 1)
    return weight_cost + distance_cost
'''

'''# 2.5
def add_task(task_list, task_name, priority="medium"):
    task_list.append({
        "name": task_name,
        "priority": priority,
        "completed": False
    })


def complete_task(task_list, task_name):
    for task in task_list:
        if task["name"] == task_name:
            task["completed"] = True
'''

# =========================
# Частина 3: Складні
# =========================

'''# 3.1 Бібліотека
def add_book(library, title, author, year, genre):
    library.append({
        "title": title,
        "author": author,
        "year": year,
        "genre": genre
    })


def find_books_by_author(library, author):
    return [b for b in library if b["author"] == author]


def find_books_by_genre(library, genre):
    return [b for b in library if b["genre"] == genre]


def get_books_published_after(library, year):
    return [b for b in library if b["year"] > year]


def get_library_statistics(library):
    authors = {}
    genres = {}

    for b in library:
        authors[b["author"]] = authors.get(b["author"], 0) + 1
        genres[b["genre"]] = genres.get(b["genre"], 0) + 1

    return {
        "total_books": len(library),
        "authors": authors,
        "genres": genres
    }
'''

'''# 3.2 Фінанси
def add_expense(expenses, date, category, amount, description=""):
    expenses.append({
        "date": date,
        "category": category,
        "amount": amount,
        "description": description
    })


def get_expenses_by_category(expenses, category):
    return [e for e in expenses if e["category"] == category]


def get_monthly_summary(expenses, year, month):
    total = 0
    for e in expenses:
        d, m, y = e["date"].split(".")
        if int(y) == year and int(m) == month:
            total += e["amount"]
    return total


def get_category_statistics(expenses):
    total = sum(e["amount"] for e in expenses)
    stats = {}

    for e in expenses:
        stats[e["category"]] = stats.get(e["category"], 0) + e["amount"]

    for k in stats:
        stats[k] = round((stats[k] / total) * 100, 1)

    return stats'''


'''# 3.3 Студенти
def add_student(students, name, group):
    students.append({
        "name": name,
        "group": group,
        "grades": {}
    })


def add_grade(students, name, subject, grade):
    for s in students:
        if s["name"] == name:
            s["grades"].setdefault(subject, []).append(grade)


def get_student_gpa(students, name):
    for s in students:
        if s["name"] == name:
            grades = [g for sub in s["grades"].values() for g in sub]
            return sum(grades) / len(grades) if grades else 0


def get_group_gpa(students, group):
    gpas = [get_student_gpa(students, s["name"]) for s in students if s["group"] == group]
    return sum(gpas) / len(gpas) if gpas else 0


def get_subject_statistics(students, subject):
    grades = []
    for s in students:
        grades.extend(s["grades"].get(subject, []))
    return {
        "average": sum(grades)/len(grades) if grades else 0,
        "max": max(grades) if grades else 0,
        "min": min(grades) if grades else 0
    }


def generate_report(students):
    report = ""
    for s in students:
        report += f"{s['name']} ({s['group']}):\n"
        for sub, grades in s["grades"].items():
            report += f"  {sub}: {grades}\n"
        report += f"  GPA: {get_student_gpa(students, s['name']):.2f}\n\n"
    return report'''
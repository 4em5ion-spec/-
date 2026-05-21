'''# =========================
# Частина 1: Легкі завдання
# =========================

# 1.1 Фільтрація додатних чисел
def filter_positive(numbers):
    return [x for x in numbers if x > 0]

# 1.2 Довжини слів
def word_lengths(words):
    return [len(w) for w in words]

# 1.3 Словник квадратів
def squares_dict(nums):
    return {x: x**2 for x in nums}

# 1.4 Перетин списків (унікальні)
def common_elements(list1, list2):
    return list({x for x in list1 if x in list2})

# 1.5 Форматування телефонів
def normalize_numbers(raw_numbers):
    return [
        "+380" + "".join(filter(str.isdigit, num))[-9:]
        for num in raw_numbers
    ]

# 1.6 Унікальні символи
def unique_chars(text):
    return {ch for ch in text}

# 1.7 Слова на літеру
def words_starting_with(word_list, letter):
    return {w for w in word_list if w.lower().startswith(letter.lower())}

# 1.8 Сума квадратів (генератор)
def sum_of_squares(numbers):
    return sum(x*x for x in numbers)

# 1.9 Генератор парних
def even_range(start, end):
    return list(x for x in range(start, end+1) if x % 2 == 0)

# 1.10 Довжина найдовшого слова
def longest_word_length(sentences):
    return max(len(word) for s in sentences for word in s.split())


# =========================
# Частина 2: Середні
# =========================

# 2.1 namedtuple
from collections import namedtuple

Student = namedtuple("Student", ["first_name", "last_name", "group", "average_mark"])

def get_best_student(students):
    if not students:
        return None
    best = max(students, key=lambda s: s.average_mark)
    return f"{best.last_name} {best.first_name[0]}."

# 2.2 defaultdict
from collections import defaultdict

def group_products(products):
    result = defaultdict(list)
    for p in products:
        result[p["category"]].append(p["name"])
    return result

# 2.3 Counter
from collections import Counter

def analyze_text(text, n):
    words = [
        w.strip(".,!?;:").lower()
        for w in text.split()
    ]
    counts = Counter(words)
    return counts.most_common(n)

# 2.4 Генератор факторіалів
def factorial_gen(max_n):
    fact = 1
    for i in range(0, max_n + 1):
        if i == 0:
            yield 1
        else:
            fact *= i
            yield fact

# 2.5 Генератор чанків
def read_in_chunks(total_size, chunk_size=1024):
    read = 0
    while read < total_size:
        size = min(chunk_size, total_size - read)
        yield "A" * size
        read += size


# =========================
# Частина 3: Складні
# =========================

# 3.1 Топ IP (генератор + Counter)
def log_generator(data):
    for line in data:
        yield line

def find_top_ips(log_gen, top_n):
    counter = Counter()
    for ip in log_gen:
        counter[ip] += 1
    return counter.most_common(top_n)

# 3.2 Парсер конфігів
def parse_config(config_lines):
    section = "GLOBAL"
    for line in config_lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1]
        elif "=" in line:
            key, value = map(str.strip, line.split("=", 1))
            yield (section, key, value)

# 3.3 Ітератор вкладених списків
class NestedListIterator:
    def __init__(self, nested_list):
        self.stack = list(reversed(nested_list))

    def __iter__(self):
        return self

    def __next__(self):
        while self.stack:
            current = self.stack.pop()
            if isinstance(current, list):
                self.stack.extend(reversed(current))
            else:
                return current
        raise StopIteration'''
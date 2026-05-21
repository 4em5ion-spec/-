'''"# Звичайна функція
def square(x):
    return x ** 2
# Еквівалентна lambda-функція
square_lambda = lambda x: x ** 2

print(square(5))         # 25
print(square_lambda(5))  # 25
'''
'''
temps = list(map(int, input().split()))
average = sum(temps) / len(temps)
count = 0
for t in temps:
    if t >= average:
        count += 1
print(count)
'''
'''
```python
# =========================
# Частина 1: Легкі завдання
# =========================

# 1.1
is_even = lambda x: x % 2 == 0

# 1.2
greet = lambda name, greeting="Hello": f"{greeting}, {name}!"

# 1.3
area = lambda a, b: float(a * b)

# 1.4
is_palindrome = lambda s: (s := s.lower().replace(" ", "")) == s[::-1]

# 1.5
prices = [100, 200, 300, 400]
discounted_prices = list(map(lambda x: round(x * 0.85, 2), prices))

# 1.6
words = ["cat", "elephant", "dog", "house", "algorithm"]
long_words = list(filter(lambda w: len(w) > 4, words))

# 1.7
grades = [45, 85, 90, 67, 33, 78, 92, 100, 55]
processed_grades = list(
    map(lambda g: round((g / 100) * 12),
        filter(lambda g: g >= 60, grades))
)

# 1.8
def sum_to_n(n):
    if n <= 0:
        return 0
    return n + sum_to_n(n - 1)

# 1.9
def count_digits(n):
    if n < 10:
        return 1
    return 1 + count_digits(n // 10)

# 1.10
def reverse_number(n, rev=0):
    if n == 0:
        return rev
    return reverse_number(n // 10, rev * 10 + n % 10)


# =========================
# Частина 2: Середні завдання
# =========================

# 2.1
def flexible_average(*args):
    nums = list(filter(lambda x: isinstance(x, (int, float)), args))
    if not nums:
        return None
    return sum(nums) / len(nums)

# 2.2
def make_html_tag(tag_name, content, **attributes):
    attrs = []
    for k, v in attributes.items():
        if k == "class_":
            k = "class"
        attrs.append(f'{k}="{v}"')
    attrs_str = " " + " ".join(attrs) if attrs else ""
    return f"<{tag_name}{attrs_str}>{content}</{tag_name}>"

# 2.3
def find_max(lst):
    if len(lst) == 1:
        return lst[0]
    sub_max = find_max(lst[1:])
    return lst[0] if lst[0] > sub_max else sub_max

# 2.4
def logged(func):
    def wrapper(*args, **kwargs):
        print(f"Calling function {func.__name__} with arguments {args} {kwargs}")
        result = func(*args, **kwargs)
        print(f"Function {func.__name__} returned {result}")
        return result
    return wrapper

@logged
def add(a, b):
    return a + b

# приклад виклику:
# add(5, 3)

# 2.5
students = [
    {'name': 'Anna', 'age': 22, 'avg_grade': 91},
    {'name': 'Bob', 'age': 19, 'avg_grade': 78},
    {'name': 'Charlie', 'age': 23, 'avg_grade': 88}
]

selected_students = list(
    map(lambda s: s['name'],
        filter(lambda s: s['age'] > 20 and s['avg_grade'] > 85, students))
)


# =========================
# Частина 3: Складні завдання
# =========================

# 3.1
def permutations(items):
    if len(items) == 0:
        return [[]]
    if len(items) == 1:
        return [items]

    result = []
    for i in range(len(items)):
        current = items[i]
        rest = items[:i] + items[i+1:]
        for p in permutations(rest):
            result.append([current] + p)
    return result

# 3.2
def map_tree(node, func):
    return {
        'value': func(node['value']),
        'children': list(map(lambda child: map_tree(child, func), node['children']))
    }

# 3.3
def memoize(func):
    cache = {}
    def wrapper(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    return wrapper

@memoize
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

```

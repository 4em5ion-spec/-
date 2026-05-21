'''# =========================
# Частина 1: Легкі завдання
# =========================

# 1.1 Реверс рядка через стек
class Stack:
    def __init__(self):
        self.items = []

    def push(self, x):
        self.items.append(x)

    def pop(self):
        return self.items.pop() if self.items else None

    def is_empty(self):
        return len(self.items) == 0

def reverse_string(text):
    stack = Stack()
    for ch in text:
        stack.push(ch)
    result = ""
    while not stack.is_empty():
        result += stack.pop()
    return result

# 1.2 Паліндром через стек
def is_palindrome(text):
    clean = "".join(ch.lower() for ch in text if ch != " ")
    stack = Stack()
    for ch in clean:
        stack.push(ch)
    reversed_text = ""
    while not stack.is_empty():
        reversed_text += stack.pop()
    return clean == reversed_text

# 1.3 Черга заявок
def process_requests(requests):
    queue = list(requests)
    result = []
    while queue:
        result.append(queue.pop(0))
    return result

# 1.4 Розмір стеку без len()
def stack_size(stack):
    temp = []
    count = 0
    while stack:
        temp.append(stack.pop())
        count += 1
    while temp:
        stack.append(temp.pop())
    return count

# 1.5 Пріоритетна черга
def simple_priority_queue(tasks):
    tasks_sorted = sorted(tasks, key=lambda x: x[0])
    return [t[1] for t in tasks_sorted]

# 1.6 Сортування парних (вибором)
def sort_even_numbers(numbers):
    evens = [x for x in numbers if x % 2 == 0]
    for i in range(len(evens)):
        min_idx = i
        for j in range(i+1, len(evens)):
            if evens[j] < evens[min_idx]:
                min_idx = j
        evens[i], evens[min_idx] = evens[min_idx], evens[i]
    return evens

# 1.7 Лінійний пошук
def linear_search_count(arr, target):
    count = 0
    for i, val in enumerate(arr):
        count += 1
        if val == target:
            return i, count
    return -1, count

# 1.8 Бінарний пошук
def binary_search_steps(arr, target):
    left, right = 0, len(arr) - 1
    steps = []
    while left <= right:
        mid = (left + right) // 2
        steps.append(mid)
        if arr[mid] == target:
            return steps, mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return steps, -1

# 1.9 Бульбашка оптимізована
def bubble_sort_optimized(arr):
    n = len(arr)
    iterations = 0
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        iterations += 1
        if not swapped:
            break
    return arr, iterations

# 1.10 Мін і макс
def find_min_max(arr):
    if not arr:
        return None
    min_val = max_val = arr[0]
    for x in arr[1:]:
        if x < min_val:
            min_val = x
        if x > max_val:
            max_val = x
    return min_val, max_val


# =========================
# Частина 2: Середні
# =========================

# 2.1 RPN калькулятор
def rpn_calculator(expression):
    stack = []
    for token in expression.split():
        if token in "+-*/":
            b = stack.pop()
            a = stack.pop()
            if token == "+": stack.append(a + b)
            elif token == "-": stack.append(a - b)
            elif token == "*": stack.append(a * b)
            elif token == "/": stack.append(int(a / b))
        else:
            stack.append(int(token))
    return stack[0]

# 2.2 Черга з таймаутом
def queue_with_timeout(customers, service_time):
    current_time = 0
    served = 0
    lost = 0

    for arrival, max_wait in customers:
        if current_time < arrival:
            current_time = arrival
        wait = current_time - arrival
        if wait <= max_wait:
            served += 1
            current_time += service_time
        else:
            lost += 1

    return served, lost

# 2.3 Сортування за критеріями
def multi_criteria_sort(students):
    return sorted(students, key=lambda s: (-s["grade"], -s["attendance"], s["name"]))

# 2.4 Гібридне сортування
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
    return arr

def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def hybrid_sort(arr, threshold=10):
    parts = [arr[i:i+threshold] for i in range(0, len(arr), threshold)]
    sorted_parts = []
    for part in parts:
        if len(part) <= threshold:
            sorted_parts.extend(insertion_sort(part))
        else:
            sorted_parts.extend(selection_sort(part))
    return sorted(sorted_parts)

# 2.5 Аналіз складності
import time

def complexity_analyzer(sort_func, sizes):
    for size in sizes:
        arr = [random.randint(0, 1000) for _ in range(size)]
        start = time.time()
        sort_func(arr.copy())
        end = time.time()
        print(f"Розмір {size}: {round(end-start,4)} сек")


# =========================
# Частина 3: Складні
# =========================

# 3.1 Планувальник задач
def schedule_tasks(tasks):
    completed = []
    total_time = 0

    while tasks:
        for task in sorted(tasks, key=lambda t: t["priority"]):
            if all(dep in completed for dep in task["dependencies"]):
                completed.append(task["id"])
                total_time += task["duration"]
                tasks.remove(task)
                break

    return completed, total_time

# 3.2 Оптимізація маршруту (спрощено)
def optimize_route(deliveries, travel_time):
    current = deliveries[0]
    route = [current["id"]]
    time = current["service"]

    remaining = deliveries[1:]

    while remaining:
        remaining.sort(key=lambda x: x["priority"])
        next_d = remaining.pop(0)
        time += travel_time.get((current["address"], next_d["address"]), 0)
        time += next_d["service"]
        route.append(next_d["id"])
        current = next_d

    return route, time

# 3.3 (теоретичне завдання - код як приклад тесту)
def test_sorting():
    arr = [random.randint(0,1000) for _ in range(1000)]
    print(bubble_sort_optimized(arr.copy())[1])
    print(sorted(arr))'''
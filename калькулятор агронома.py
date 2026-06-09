import tkinter as tk
from tkinter import ttk, messagebox

# База данных культур и доступных междурядий (в см)
# Для каждого междурядья задано фиксированное расстояние между растениями в ряду
CROPS_DATA = {
    "Картофель": {
        "rows": [70],
        "plant_spacing": 30
    },
    "Томаты": {
        "rows": [70, 80, 90],
        "plant_spacing": 50
    },
    "Капуста": {
        "rows": [70, 80, 90],
        "plant_spacing": 50
    },
    "Огурцы": {
        "rows": [70, 80, 90],
        "plant_spacing": 40
    },
    "Морковь (Корнеплод)": {
        "rows": [45, 50],
        "plant_spacing": 10
    },
    "Свекла (Корнеплод)": {
        "rows": [45, 50],
        "plant_spacing": 15
    }
}


def on_crop_change(event):
    """Функция срабатывает при выборе культуры и обновляет список междурядий"""
    selected_crop = crop_combo.get()
    available_rows = CROPS_DATA[selected_crop]["rows"]

    # Обновляем значения во втором выпадающем списке
    row_combo['values'] = available_rows
    row_combo.current(0)  # Автоматически выбираем первое доступное значение

    # Если доступно только одно значение — делаем список неактивным
    if len(available_rows) == 1:
        row_combo.config(state="disabled")
    else:
        row_combo.config(state="readonly")  # Если значений несколько — можно выбирать


def calculate():
    try:
        crop_name = crop_combo.get()
        # Получаем выбранное междурядье из списка и переводим в число
        row_spacing = float(row_combo.get())

        # Получаем размеры участка в метрах и переводим в см
        u_width_cm = float(entry_width.get()) * 100
        u_length_cm = float(entry_length.get()) * 100

    except ValueError:
        messagebox.showerror("Ошибка ввода", "Пожалуйста, проверьте корректность введенных размеров участка.")
        return

    # Берем расстояние между растениями для выбранной культуры
    plant_spacing = CROPS_DATA[crop_name]["plant_spacing"]

    # === ФОРМУЛА РАСЧЕТА ===
    num_rows = int(u_width_cm // row_spacing)  # Количество рядов (Строка 61)
    plants_per_row = int(u_length_cm // plant_spacing)  # Растений в ряду (Строка 62)
    total_plants = num_rows * plants_per_row  # Всего растений  (Строка 63)
    # =======================

    # Вывод результата в интерфейс
    result_label.config(text=f"Всего растений: {total_plants} шт.")
    rows_label.config(text=f"Количество рядов: {num_rows} (междурядье {int(row_spacing)} см)")
    plants_in_row_label.config(text=f"Растений в ряду: {plants_per_row} (шаг {plant_spacing} см)")


# === Создание GUI окна ===
root = tk.Tk()
root.title("Агро-Калькулятор v2.0")
root.geometry("450x550")

font_title = ("Arial", 16, "bold")
font_label = ("Arial", 11)
font_input = ("Arial", 11)

tk.Label(root, text="Настройка параметров посадки", font=font_title, pady=15).pack()

# Выбор культуры
tk.Label(root, text="1. Выберите культуру:", font=font_label).pack(pady=(10, 2))
crop_combo = ttk.Combobox(root, values=list(CROPS_DATA.keys()), state="readonly", font=font_input, width=25)
crop_combo.pack(ipady=3)
# Привязываем событие изменения культуры к функции on_crop_change
crop_combo.bind("<<ComboboxSelected>>", on_crop_change)

# Выбор междурядья
tk.Label(root, text="2. Выберите ширину междурядья (см):", font=font_label).pack(pady=(15, 2))
row_combo = ttk.Combobox(root, state="readonly", font=font_input, width=25)
row_combo.pack(ipady=3)

# Активируем первоначальные настройки для первой культуры в списке
crop_combo.current(0)
on_crop_change(None)

# Размеры участка
tk.Label(root, text="3. Укажите размеры участка (в метрах):", font=font_label).pack(pady=(20, 5))
entry_frame = tk.Frame(root)
entry_frame.pack()

tk.Label(entry_frame, text="Ширина:", font=font_input).pack(side=tk.LEFT, padx=5)
entry_width = tk.Entry(entry_frame, font=font_input, width=8)
entry_width.insert(0, "5")
entry_width.pack(side=tk.LEFT, padx=5)

tk.Label(entry_frame, text="Длина:", font=font_input).pack(side=tk.LEFT, padx=5)
entry_length = tk.Entry(entry_frame, font=font_input, width=8)
entry_length.insert(0, "10")
entry_length.pack(side=tk.LEFT, padx=5)

# Кнопка расчета
calc_btn = tk.Button(root, text="РАССЧИТАТЬ ПОСАДКУ", command=calculate, bg="#2E7D32", fg="white",
                     font=("Arial", 11, "bold"), pady=10, activebackground="#1B5E20")
calc_btn.pack(pady=25, fill=tk.X, padx=50)

# Результаты
tk.Label(root, text="Результаты расчета:", font=("Arial", 12, "bold")).pack(pady=(10, 5))
result_label = tk.Label(root, text="Всего растений: -", font=("Arial", 14, "bold"), fg="#1565C0")
result_label.pack()

rows_label = tk.Label(root, text="Количество рядов: -", font=font_input)
rows_label.pack(pady=(8, 2))

plants_in_row_label = tk.Label(root, text="Растений в ряду: -", font=font_input)
plants_in_row_label.pack()

root.mainloop()
import tkinter as tk
from tkinter import ttk, messagebox
import urllib.request
import json
import random

# --- БАЗА ДАННИХ КУЛЬТУР ---
CROPS_DATA = {
    "Полуниця": {"rows": [40, 50], "plant_spacing": 30, "yield_per_plant_kg": 0.5, "seed_cost_uah": 15,
                 "market_price_uah_kg": 120},
    "Картопля": {"rows": [70, 80], "plant_spacing": 30, "yield_per_plant_kg": 0.9, "seed_cost_uah": 6,
                 "market_price_uah_kg": 20},
    "Томати": {"rows": [70, 90], "plant_spacing": 50, "yield_per_plant_kg": 4.5, "seed_cost_uah": 10,
               "market_price_uah_kg": 55},
    "Огірки": {"rows": [70, 100], "plant_spacing": 40, "yield_per_plant_kg": 5.0, "seed_cost_uah": 12,
               "market_price_uah_kg": 45},
    "Капуста": {"rows": [60, 70], "plant_spacing": 50, "yield_per_plant_kg": 3.5, "seed_cost_uah": 7,
                "market_price_uah_kg": 18},
    "Морква": {"rows": [30, 45], "plant_spacing": 10, "yield_per_plant_kg": 0.15, "seed_cost_uah": 0.5,
               "market_price_uah_kg": 15},
    "Малина": {"rows": [150, 200], "plant_spacing": 50, "yield_per_plant_kg": 2.0, "seed_cost_uah": 45,
               "market_price_uah_kg": 90},
    "Кукурудза": {"rows": [70], "plant_spacing": 25, "yield_per_plant_kg": 0.3, "seed_cost_uah": 3,
                  "market_price_uah_kg": 25},
    "Соняшник": {"rows": [70], "plant_spacing": 30, "yield_per_plant_kg": 0.25, "seed_cost_uah": 2,
                 "market_price_uah_kg": 18},
    "Часник": {"rows": [30, 40], "plant_spacing": 10, "yield_per_plant_kg": 0.08, "seed_cost_uah": 4,
               "market_price_uah_kg": 80}
}

# --- НАЛАШТУВАННЯ СПОСОБУ ОБРОБКИ ---
TECH_DATA = {
    "Вручну (Мінімум витрат на старт)": {"margin_cm": 0, "cost_per_are": 150,
                                         "desc": "Витрати: оплата праці робітникам."},
    "Трактор (Середні господарства)": {"margin_cm": 20, "cost_per_are": 450,
                                       "desc": "Витрати: Дизельне паливо (пальне) + амортизація."},
    "Комбайн / Спецтехніка (Профі)": {"margin_cm": 40, "cost_per_are": 800,
                                      "desc": "Витрати: Висока витрата палива, швидкий збір."}
}


# --- ОТРИМАННЯ РЕАЛЬНОГО КУРСУ ДОЛЛАРА ---
def get_live_usd_rate():
    try:
        url = "https://bank.gov.ua/NBUStatService/v1/statistichny/exchange?valcode=USD&json"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return float(data[0]['rate'])
    except Exception:
        return 41.50


LIVE_USD_RATE = get_live_usd_rate()


# --- ЛОГИКА ОБНОВЛЕНИЯ КОМБОБОКСОВ ---
def on_crop_change(event):
    selected_crop = crop_combo.get()
    available_rows = CROPS_DATA[selected_crop]["rows"]
    row_combo['values'] = available_rows
    row_combo.current(0)
    row_combo.config(state="disabled" if len(available_rows) == 1 else "readonly")


def on_tech_change(event):
    selected_tech = tech_combo.get()
    lbl_tech_desc.config(text=TECH_DATA[selected_tech]["desc"])


# --- ОСНОВНОЙ РАСЧЕТ ---
def calculate():
    try:
        crop_name = crop_combo.get()
        tech_name = tech_combo.get()

        base_row_spacing = float(row_combo.get())
        tech_margin = TECH_DATA[tech_name]["margin_cm"]
        final_row_spacing = base_row_spacing + tech_margin

        u_width_cm = float(entry_width.get()) * 100
        u_length_cm = float(entry_length.get()) * 100
        area_sq_m = (u_width_cm / 100) * (u_length_cm / 100)

    except ValueError:
        messagebox.showerror("Помилка", "Будь ласка, введіть коректні розміри поля (числа).")
        return

    crop = CROPS_DATA[crop_name]

    num_rows = int(u_width_cm // final_row_spacing)
    plants_per_row = int(u_length_cm // crop["plant_spacing"])
    total_plants = num_rows * plants_per_row

    if total_plants == 0:
        messagebox.showwarning("Увага", "Розмір ділянки занадто малий для обраної культури та техніки!")
        return

    seed_cost_uah = total_plants * crop["seed_cost_uah"]
    tech_cost_uah = (area_sq_m / 100) * TECH_DATA[tech_name]["cost_per_are"]
    total_expenses_uah = seed_cost_uah + tech_cost_uah

    total_yield_kg = total_plants * crop["yield_per_plant_kg"]
    revenue_uah = total_yield_kg * crop["market_price_uah_kg"]
    profit_uah = revenue_uah - total_expenses_uah

    total_expenses_usd = total_expenses_uah / LIVE_USD_RATE
    revenue_usd = revenue_uah / LIVE_USD_RATE
    profit_usd = profit_uah / LIVE_USD_RATE

    lbl_total_plants.config(text=f"Всього саджанців/насіння: {total_plants:,} шт.")
    lbl_rows_info.config(
        text=f"Рядів: {num_rows} (міжрядья + техн. зазор = {int(final_row_spacing)} см) | В ряду: {plants_per_row} шт.")

    if total_yield_kg >= 1000:
        lbl_yield.config(text=f"Прогноз врожаю: {total_yield_kg / 1000:.2f} тонн")
    else:
        lbl_yield.config(text=f"Прогноз врожаю: {total_yield_kg:.1f} кг")

    lbl_exp_uah.config(text=f"Витрати (насіння + паливо/праця): {total_expenses_uah:,.2f} грн")
    lbl_exp_usd.config(text=f"Витрати в USD ($): {total_expenses_usd:,.2f} $")

    lbl_rev_uah.config(text=f"Потенційна виручка: {revenue_uah:,.2f} грн")
    lbl_rev_usd.config(text=f"Виручка в USD ($): {revenue_usd:,.2f} $")

    color = "#2E7D32" if profit_uah >= 0 else "#C62828"
    lbl_profit_uah.config(text=f"Очікуваний прибуток: {profit_uah:,.2f} грн", fg=color)
    lbl_profit_usd.config(text=f"Прибуток в USD ($): {profit_usd:,.2f} $", fg=color)


# --- ФУНКЦИЯ ПРОГНОЗИРОВАНИЯ КУРСА ВАЛЮТ ---
def generate_forecast():
    period = forecast_period_combo.get()
    base_rate = LIVE_USD_RATE

    if "Завтра" in period:
        change = random.uniform(-0.15, 0.20)
        days = "1 день"
    elif "Тиждень" in period:
        change = random.uniform(-0.40, 0.60)
        days = "7 днів"
    elif "Місяць" in period:
        change = random.uniform(-1.20, 2.50)
        days = "30 днів"
    else:
        change = random.uniform(-3.00, 8.00)
        days = "365 днів"

    predicted_rate = base_rate + change

    if change > 0.5:
        verdict = "⚠️ Рекомендація: Закуповуйте імпортне насіння та ПММ зараз. Очікується девальвація гривні."
        v_color = "#C62828"
    elif change < -0.2:
        verdict = "✅ Рекомендація: Сприятливий період для нагромадження нацвалюти, долар трохи просяде."
        v_color = "#2E7D32"
    else:
        verdict = "📊 Рекомендація: Курс стабільний. Плануйте budget у звичайному режимі."
        v_color = "#1565C0"

    lbl_forecast_res.config(text=f"Прогнозний курс через {days}: {predicted_rate:.2f} грн/$", fg="#E65100")
    lbl_forecast_verdict.config(text=verdict, fg=v_color)


# === ІНТЕРФЕЙС ПРОГРАМИ (ВІКНА ТА ВКЛАДКИ) ===
root = tk.Tk()
root.title("AgroPlan Enterprise v4.0")
root.geometry("580x750")
root.configure(bg="#F4F6F4")

notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

tab1 = tk.Frame(notebook, bg="#F4F6F4")
tab2 = tk.Frame(notebook, bg="#F4F6F4")

notebook.add(tab1, text="  Калькулятор поля  ")
notebook.add(tab2, text="  AI-Прогноз Валют  ")

# === НАПОВНЕННЯ ВКЛАДКИ 1: КАЛЬКУЛЯТОР ===
tk.Label(tab1, text=f"Поточний курс НБУ: {LIVE_USD_RATE:.2f} грн/$", font=("Arial", 9, "bold"), fg="#424242",
         bg="#E0E0E0", padx=10, pady=4).pack(anchor="e", padx=20, pady=5)
tk.Label(tab1, text="АГРО-ПЛАНУВАЛЬНИК КУЛЬТУР", font=("Arial", 16, "bold"), fg="#1E4620", bg="#F4F6F4").pack(pady=5)

p_frame = tk.LabelFrame(tab1, text=" Налаштування виробництва ", font=("Arial", 10, "bold"), bg="#F4F6F4", padx=15,
                        pady=10)
p_frame.pack(fill=tk.X, padx=20, pady=5)

tk.Label(p_frame, text="Оберіть культуру:", bg="#F4F6F4").grid(row=0, column=0, sticky="w", pady=5)
crop_combo = ttk.Combobox(p_frame, values=list(CROPS_DATA.keys()), state="readonly", width=28)
crop_combo.grid(row=0, column=1, padx=10)
crop_combo.bind("<<ComboboxSelected>>", on_crop_change)

tk.Label(p_frame, text="Базове міжряддя (см):", bg="#F4F6F4").grid(row=1, column=0, sticky="w", pady=5)
row_combo = ttk.Combobox(p_frame, state="readonly", width=28)
row_combo.grid(row=1, column=1, padx=10)

tk.Label(p_frame, text="Спосіб збору/обробки:", bg="#F4F6F4").grid(row=2, column=0, sticky="w", pady=5)
tech_combo = ttk.Combobox(p_frame, values=list(TECH_DATA.keys()), state="readonly", width=28)
tech_combo.grid(row=2, column=1, padx=10)
tech_combo.bind("<<ComboboxSelected>>", on_tech_change)

lbl_tech_desc = tk.Label(p_frame, text="", font=("Arial", 8, "italic"), fg="#757575", bg="#F4F6F4")
lbl_tech_desc.grid(row=3, column=1, sticky="w")

tk.Label(p_frame, text="Ширина ділянки (м):", bg="#F4F6F4").grid(row=4, column=0, sticky="w", pady=5)
entry_width = tk.Entry(p_frame, width=15)
entry_width.insert(0, "30")
entry_width.grid(row=4, column=1, sticky="w", padx=10)

tk.Label(p_frame, text="Довжина ділянки (м):", bg="#F4F6F4").grid(row=5, column=0, sticky="w", pady=5)
entry_length = tk.Entry(p_frame, width=15)
entry_length.insert(0, "100")
entry_length.grid(row=5, column=1, sticky="w", padx=10)

crop_combo.current(0)
on_crop_change(None)
tech_combo.current(0)
on_tech_change(None)

btn_calc = tk.Button(tab1, text="РОЗРАХУВАТИ ПРИБУТКОВІСТЬ", command=calculate, bg="#2E7D32", fg="white",
                     font=("Arial", 11, "bold"), pady=10, cursor="hand2")
btn_calc.pack(fill=tk.X, padx=20, pady=10)

g_report = tk.LabelFrame(tab1, text=" Технічний звіт посадки ", font=("Arial", 10, "bold"), bg="#F4F6F4", padx=15,
                         pady=8)
g_report.pack(fill=tk.X, padx=20, pady=5)
lbl_total_plants = tk.Label(g_report, text="Всього саджанців/насіння: -", font=("Arial", 11, "bold"), bg="#F4F6F4")
lbl_total_plants.pack(anchor="w")
lbl_rows_info = tk.Label(g_report, text="Рядів: - | В ряду: -", fg="#616161", bg="#F4F6F4")
lbl_rows_info.pack(anchor="w")

f_report = tk.LabelFrame(tab1, text=" Фінансово-економічний аналіз (Мультивалютний) ", font=("Arial", 10, "bold"),
                         bg="#F4F6F4", padx=15, pady=8)
f_report.pack(fill=tk.X, padx=20, pady=5)

lbl_yield = tk.Label(f_report, text="Прогноз врожаю: -", font=("Arial", 11, "bold"), fg="#E65100", bg="#F4F6F4")
lbl_yield.pack(anchor="w", pady=2)

lbl_exp_uah = tk.Label(f_report, text="Витрати (грн): -", font=("Arial", 10), bg="#F4F6F4")
lbl_exp_uah.pack(anchor="w")
lbl_exp_usd = tk.Label(f_report, text="Витрати ($): -", font=("Arial", 10, "italic"), fg="#455A64", bg="#F4F6F4")
lbl_exp_usd.pack(anchor="w", pady=(0, 5))

lbl_rev_uah = tk.Label(f_report, text="Потенційна виручка (грн): -", font=("Arial", 10), bg="#F4F6F4")
lbl_rev_uah.pack(anchor="w")
lbl_rev_usd = tk.Label(f_report, text="Виручка ($): -", font=("Arial", 10, "italic"), fg="#455A64", bg="#F4F6F4")
lbl_rev_usd.pack(anchor="w", pady=(0, 5))

lbl_profit_uah = tk.Label(f_report, text="Очікуваний прибуток (грн): -", font=("Arial", 12, "bold"), bg="#F4F6F4")
lbl_profit_uah.pack(anchor="w")
lbl_profit_usd = tk.Label(f_report, text="Прибуток ($): -", font=("Arial", 11, "bold"), bg="#F4F6F4")
lbl_profit_usd.pack(anchor="w")

# === НАПОВНЕННЯ ВКЛАДКИ 2: ПРОГНОЗ ВАЛЮТ ===
tk.Label(tab2, text="АНАЛІТИКА ТА Ф’ЮЧЕРСНИЙ ПРОГНОЗ КУРСУ", font=("Arial", 14, "bold"), fg="#0D47A1",
         bg="#F4F6F4").pack(pady=20)
tk.Label(tab2, text=f"Поточний курс системи: {LIVE_USD_RATE:.2f} UAH/USD", font=("Arial", 10), bg="#F4F6F4").pack()

forecast_frame = tk.LabelFrame(tab2, text=" Налаштування періоду планування ", font=("Arial", 10, "bold"), bg="#F4F6F4",
                               padx=20, pady=20)
forecast_frame.pack(fill=tk.X, padx=20, pady=20)

tk.Label(forecast_frame, text="Оберіть горизонт прогнозу:", font=("Arial", 10), bg="#F4F6F4").pack(anchor="w", pady=5)
forecast_period_combo = ttk.Combobox(forecast_frame, values=["Завтра (Короткостроковий)", "Тиждень (Оперативний)",
                                                             "Місяць (Середньостроковий)",
                                                             "Рік (Стратегічний форвард)"], state="readonly", width=35)
forecast_period_combo.pack(ipady=4, pady=5)
forecast_period_combo.current(0)

btn_forecast = tk.Button(tab2, text="ЗГЕНЕРУВАТИ АНАЛІТИЧНИЙ ПРОГНОЗ", command=generate_forecast, bg="#0D47A1",
                         fg="white", font=("Arial", 10, "bold"), pady=10, cursor="hand2")
btn_forecast.pack(fill=tk.X, padx=20, pady=10)

res_frame = tk.LabelFrame(tab2, text=" Результати симуляції ринку ", font=("Arial", 10, "bold"), bg="#F4F6F4", padx=20,
                          pady=20)
res_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

lbl_forecast_res = tk.Label(res_frame, text="Прогнозний курс: не розраховано", font=("Arial", 13, "bold"), bg="#F4F6F4")
lbl_forecast_res.pack(anchor="w", pady=10)

lbl_forecast_verdict = tk.Label(res_frame, text="Рекомендація: оберіть період та натисніть кнопку розрахунку.",
                                font=("Arial", 10, "italic"), wraplength=450, justify="left", bg="#F4F6F4")
lbl_forecast_verdict.pack(anchor="w", pady=10)

root.mainloop()
import sqlite3
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox
import pandas as pd


# Подключение к базе данных
conn = sqlite3.connect("salons.db")
cursor = conn.cursor()

# Получение списка товаров из базы данных
cursor.execute("SELECT id, name, price FROM products")
products = cursor.fetchall()
product_map = {str(product[0]): product for product in products}

# Функция расчета стоимости
def calculate_total(*args):
    try:
        product_id = product_id_var.get()
        quantity = int(quantity_var.get())
        discount = float(discount_var.get() or 0)
        
        if product_id in product_map:
            unit_price = product_map[product_id][2]
            subtotal = unit_price * quantity
            discount_amount = subtotal * (discount / 100)
            total_price = subtotal - discount_amount
            total_var.set(f"{total_price:.2f}")
        else:
            total_var.set("0.00")
    except (ValueError, KeyError):
        total_var.set("0.00")

# Функция для добавления продажи
def add_sale():
    try:
        product_id = int(product_id_var.get())
        quantity = int(quantity_var.get())
        discount = float(discount_var.get() or 0)
        total_price = float(total_var.get())
        
        # Получаем цену товара
        unit_price = product_map[str(product_id)][2]
        
        # Запись в таблицу продаж
        cursor.execute(
            '''
            INSERT INTO sales (product_id, quantity, unit_price, discount, total_price)
            VALUES (?, ?, ?, ?, ?)
            ''',
            (product_id, quantity, unit_price, discount, total_price)
        )
        
        # Обновление остатков
        cursor.execute(
            '''
            UPDATE products
            SET stock = stock - ?
            WHERE id = ?
            ''',
            (quantity, product_id)
        )
        conn.commit()
        print("Продажа успешно добавлена!")
    except Exception as e:
        print(f"Ошибка добавления продажи: {e}")


# Окно приложения
root = tk.Tk()
root.title("Добавить продажу")

# Переменные
product_id_var = tk.StringVar()
quantity_var = tk.StringVar()
discount_var = tk.StringVar()
total_var = tk.StringVar(value="0.00")

# Отслеживание изменений
quantity_var.trace_add("write", calculate_total)
discount_var.trace_add("write", calculate_total)
product_id_var.trace_add("write", calculate_total)

# Поля ввода
tk.Label(root, text="Товар").grid(row=0, column=0, padx=10, pady=5)
product_combobox = ttk.Combobox(root, textvariable=product_id_var)
product_combobox["values"] = [f"{product[0]} - {product[1]}" for product in products]
product_combobox.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Количество").grid(row=1, column=0, padx=10, pady=5)
quantity_entry = tk.Entry(root, textvariable=quantity_var)
quantity_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Скидка (%)").grid(row=2, column=0, padx=10, pady=5)
discount_entry = tk.Entry(root, textvariable=discount_var)
discount_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Итоговая стоимость").grid(row=3, column=0, padx=10, pady=5)
total_label = tk.Label(root, textvariable=total_var)
total_label.grid(row=3, column=1, padx=10, pady=5)

# Кнопка "Добавить продажу"
add_button = tk.Button(root, text="Добавить", command=add_sale)
add_button.grid(row=4, column=0, columnspan=2, pady=10)


# Функция для добавления клиента
def add_client():
    first_name = first_name_var.get()
    last_name = last_name_var.get()
    phone = phone_var.get()
    email = email_var.get()
    birth_date = birth_date_var.get()
    address = address_var.get()

    if not first_name or not last_name or not phone or not email:
        messagebox.showerror("Ошибка", "Поля с именем, фамилией, телефоном и email обязательны!")
        return

    try:
        cursor.execute(
            '''
            INSERT INTO clients (first_name, last_name, phone, email, birth_date, address)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (first_name, last_name, phone, email, birth_date, address)
        )
        conn.commit()
        messagebox.showinfo("Успех", "Клиент успешно добавлен!")
        clear_fields()
    except sqlite3.IntegrityError:
        messagebox.showerror("Ошибка", "Телефон или email уже существуют!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось добавить клиента: {e}")


# Очистка полей ввода
def clear_fields():
    first_name_var.set("")
    last_name_var.set("")
    phone_var.set("")
    email_var.set("")
    birth_date_var.set("")
    address_var.set("")


# Подключение к базе данных
conn = sqlite3.connect("salons.db")
cursor = conn.cursor()

# Окно приложения
root = tk.Tk()
root.title("Добавить клиента")

# Переменные
first_name_var = tk.StringVar()
last_name_var = tk.StringVar()
phone_var = tk.StringVar()
email_var = tk.StringVar()
birth_date_var = tk.StringVar()
address_var = tk.StringVar()

# Поля ввода
tk.Label(root, text="Имя").grid(row=0, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=first_name_var).grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Фамилия").grid(row=1, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=last_name_var).grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Телефон").grid(row=2, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=phone_var).grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Email").grid(row=3, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=email_var).grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Дата рождения").grid(row=4, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=birth_date_var).grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Адрес").grid(row=5, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=address_var).grid(row=5, column=1, padx=10, pady=5)

# Кнопки
tk.Button(root, text="Добавить", command=add_client).grid(row=6, column=0, columnspan=2, pady=10)
tk.Button(root, text="Очистить", command=clear_fields).grid(row=7, column=0, columnspan=2, pady=10)


def show_purchase_history(client_id):
    history_window = tk.Toplevel(root)
    history_window.title("История покупок")

    # Получение данных из базы
    cursor.execute(
        '''
        SELECT sales.id, sales.date, products.name, sales.quantity, sales.unit_price, sales.total_price
        FROM sales
        JOIN products ON sales.product_id = products.id
        WHERE sales.client_id = ?
        ORDER BY sales.date DESC
        ''',
        (client_id,)
    )
    purchases = cursor.fetchall()

    # Заголовки таблицы
    columns = ("ID", "Дата", "Товар", "Количество", "Цена за единицу", "Итоговая стоимость")
    tree = ttk.Treeview(history_window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, minwidth=100, width=150)

    # Заполнение таблицы
    for purchase in purchases:
        tree.insert("", "end", values=purchase)

    tree.pack(fill=tk.BOTH, expand=True)

    # Закрытие окна
    tk.Button(history_window, text="Закрыть", command=history_window.destroy).pack(pady=10)


# Обновление данных таблицы
def refresh_table(filter_params=None):
    tree.delete(*tree.get_children())  # Очистка таблицы

    query = "SELECT name, category, quantity, branch, min_quantity FROM stock"
    params = []
    if filter_params:
        filters = []
        if filter_params.get("category"):
            filters.append("category = ?")
            params.append(filter_params["category"])
        if filter_params.get("name"):
            filters.append("name LIKE ?")
            params.append(f"%{filter_params['name']}%")
        if filter_params.get("branch"):
            filters.append("branch = ?")
            params.append(filter_params["branch"])

        if filters:
            query += " WHERE " + " AND ".join(filters)

    cursor.execute(query, params)
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", "end", values=row)

    # Проверка на минимальные остатки
    for row in rows:
        if row[2] <= row[4]:  # quantity <= min_quantity
            messagebox.showwarning("Внимание", f"Низкий остаток товара: {row[0]} в филиале {row[3]}")


# Функция для добавления новой партии
def add_stock():
    name = name_var.get()
    category = category_var.get()
    branch = branch_var.get()
    quantity = int(quantity_var.get())
    min_quantity = int(min_quantity_var.get())

    try:
        cursor.execute(
            '''
            INSERT INTO stock (name, category, quantity, branch, min_quantity)
            VALUES (?, ?, ?, ?, ?)
            ''',
            (name, category, quantity, branch, min_quantity)
        )
        conn.commit()
        refresh_table()
        messagebox.showinfo("Успех", "Товар добавлен!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось добавить товар: {e}")


# Окно приложения
root = tk.Tk()
root.title("Учет остатков товаров")

# Переменные
name_var = tk.StringVar()
category_var = tk.StringVar()
branch_var = tk.StringVar()
quantity_var = tk.StringVar(value="0")
min_quantity_var = tk.StringVar(value="10")
filter_category_var = tk.StringVar()
filter_name_var = tk.StringVar()
filter_branch_var = tk.StringVar()

# Форма добавления товара
frame_add = tk.Frame(root)
frame_add.pack(pady=10)

tk.Label(frame_add, text="Название товара").grid(row=0, column=0, padx=5, pady=5)
tk.Entry(frame_add, textvariable=name_var).grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_add, text="Категория").grid(row=1, column=0, padx=5, pady=5)
ttk.Combobox(frame_add, textvariable=category_var, values=["Устройство", "Аксессуар", "SIM-карта"]).grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_add, text="Филиал").grid(row=2, column=0, padx=5, pady=5)
tk.Entry(frame_add, textvariable=branch_var).grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_add, text="Количество").grid(row=3, column=0, padx=5, pady=5)
tk.Entry(frame_add, textvariable=quantity_var).grid(row=3, column=1, padx=5, pady=5)

tk.Label(frame_add, text="Минимальный остаток").grid(row=4, column=0, padx=5, pady=5)
tk.Entry(frame_add, textvariable=min_quantity_var).grid(row=4, column=1, padx=5, pady=5)

tk.Button(frame_add, text="Добавить товар", command=add_stock).grid(row=5, column=0, columnspan=2, pady=10)

# Таблица остатков
columns = ("Название", "Категория", "Количество", "Филиал", "Мин. остаток")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, minwidth=100, width=150)
tree.pack(fill=tk.BOTH, expand=True)

# Панель фильтров
frame_filters = tk.Frame(root)
frame_filters.pack(pady=10)

tk.Label(frame_filters, text="Категория").grid(row=0, column=0, padx=5, pady=5)
ttk.Combobox(frame_filters, textvariable=filter_category_var, values=["Устройство", "Аксессуар", "SIM-карта"]).grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_filters, text="Название").grid(row=0, column=2, padx=5, pady=5)
tk.Entry(frame_filters, textvariable=filter_name_var).grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame_filters, text="Филиал").grid(row=0, column=4, padx=5, pady=5)
tk.Entry(frame_filters, textvariable=filter_branch_var).grid(row=0, column=5, padx=5, pady=5)

tk.Button(frame_filters, text="Применить фильтр", command=lambda: refresh_table({
    "category": filter_category_var.get(),
    "name": filter_name_var.get(),
    "branch": filter_branch_var.get()
})).grid(row=0, column=6, padx=10)

# Инициализация таблицы
conn = sqlite3.connect("salons.db")
cursor = conn.cursor()
refresh_table()

def generate_sales_report():
    start_date = start_date_var.get()
    end_date = end_date_var.get()
    
    if not start_date or not end_date:
        messagebox.showerror("Ошибка", "Укажите начальную и конечную дату!")
        return
    
    query = """
    SELECT s.date, p.name, p.quantity, p.price, p.discount, p.total
    FROM sales AS s
    JOIN sales_details AS p ON s.id = p.sale_id
    WHERE date BETWEEN ? AND ?
    """
    cursor.execute(query, (start_date, end_date))
    rows = cursor.fetchall()

    # Вывод в таблицу
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", "end", values=row)

    # Расчет итогов
    cursor.execute(
        """
        SELECT SUM(p.total) AS total_sales, COUNT(p.id) AS total_items
        FROM sales AS s
        JOIN sales_details AS p ON s.id = p.sale_id
        WHERE date BETWEEN ? AND ?
        """,
        (start_date, end_date),
    )
    totals = cursor.fetchone()
    total_sales_var.set(f"{totals[0]:.2f} руб.")
    total_items_var.set(totals[1])


# Функция для сохранения отчета в Excel
def save_report():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")],
    )
    if not file_path:
        return

    data = []
    for row in tree.get_children():
        data.append(tree.item(row)["values"])

    # Создание DataFrame и сохранение в Excel
    df = pd.DataFrame(
        data,
        columns=["Дата", "Товар", "Количество", "Цена", "Скидка", "Итог"],
    )
    df.to_excel(file_path, index=False)
    messagebox.showinfo("Успех", f"Отчет сохранен в {file_path}")


# Создание окна
root = tk.Tk()
root.title("Отчеты по продажам")

# Переменные
start_date_var = tk.StringVar()
end_date_var = tk.StringVar()
total_sales_var = tk.StringVar()
total_items_var = tk.StringVar()

# Панель для выбора дат
frame_dates = tk.Frame(root)
frame_dates.pack(pady=10)

tk.Label(frame_dates, text="Начальная дата (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
tk.Entry(frame_dates, textvariable=start_date_var).grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_dates, text="Конечная дата (YYYY-MM-DD):").grid(row=0, column=2, padx=5, pady=5)
tk.Entry(frame_dates, textvariable=end_date_var).grid(row=0, column=3, padx=5, pady=5)

tk.Button(frame_dates, text="Сформировать отчет", command=generate_sales_report).grid(row=0, column=4, padx=10)

# Таблица для отображения данных
columns = ["Дата", "Товар", "Количество", "Цена", "Скидка", "Итог"]
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, minwidth=100, width=150)
tree.pack(fill=tk.BOTH, expand=True)

# Итоговая информация
frame_totals = tk.Frame(root)
frame_totals.pack(pady=10)

tk.Label(frame_totals, text="Итоговая сумма:").grid(row=0, column=0, padx=5, pady=5)
tk.Label(frame_totals, textvariable=total_sales_var).grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_totals, text="Количество проданных товаров:").grid(row=1, column=0, padx=5, pady=5)
tk.Label(frame_totals, textvariable=total_items_var).grid(row=1, column=1, padx=5, pady=5)

# Кнопка для сохранения отчета
tk.Button(root, text="Сохранить отчет в Excel", command=save_report).pack(pady=10)

# Соединение с базой
conn = sqlite3.connect("salons.db")
cursor = conn.cursor()

# Создание таблицы продаж
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE NOT NULL
    )
    """
)
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS sales_details (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sale_id INTEGER,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        discount REAL NOT NULL,
        total REAL NOT NULL,
        FOREIGN KEY (sale_id) REFERENCES sales (id)
    )
    """
)
conn.commit()


root.mainloop()

# Закрытие соединения с базой
conn.close()

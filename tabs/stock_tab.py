import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


class StockTab(tk.Frame):
    def __init__(self, parent, db_connection):
        super().__init__(parent)

        self.db_connection = db_connection
        self.parent = parent

        # Заголовок вкладки
        self.title_label = tk.Label(self, text="Учет остатков товаров", font=("Arial", 16))
        self.title_label.pack(pady=10)

        # Поля для фильтрации
        filter_frame = tk.Frame(self)
        filter_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(filter_frame, text="Категория:").grid(row=0, column=0, padx=5)
        self.category_filter = ttk.Combobox(filter_frame, values=["Все", "Устройство", "Аксессуар", "SIM-карта"], state="readonly")
        self.category_filter.set("Все")
        self.category_filter.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Филиал:").grid(row=0, column=2, padx=5)
        branches = self.get_branches()
        branches.insert(0, "Все")
        self.branch_filter = ttk.Combobox(filter_frame, values=branches, state="readonly")
        self.branch_filter.set("Все")
        self.branch_filter.grid(row=0, column=3, padx=5)

        tk.Label(filter_frame, text="Название товара:").grid(row=0, column=4, padx=5)
        names = self.get_names()
        names.insert(0, "Все")
        self.name_filter = ttk.Combobox(filter_frame, values=names, state="readonly")
        self.name_filter.set("Все")
        self.name_filter.grid(row=0, column=5, padx=5)

        filter_button = tk.Button(filter_frame, text="Фильтровать", command=self.filter_stock)
        filter_button.grid(row=0, column=6, padx=5)

        # Таблица остатков
        self.create_stock_table()

        # Кнопки управления
        button_frame = tk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=10)

        self.edit_stock_button = tk.Button(button_frame, text="Редактировать остатки", command=self.edit_stock)
        self.edit_stock_button.pack(side="left", padx=5)

        self.add_stock_button = tk.Button(button_frame, text="Добавить товары", command=self.add_stock)
        self.add_stock_button.pack(side="left", padx=5)

        # Загрузка данных
        self.load_stock()

    def create_stock_table(self):
        """Создание таблицы для отображения остатков товаров."""
        self.stock_table = ttk.Treeview(self, columns=("ID", "Название", "Категория", "Цена", "Количество", "Филиал", "Минимум"), show="headings")
        self.stock_table.heading("ID", text="ID")
        self.stock_table.heading("Название", text="Название")
        self.stock_table.heading("Категория", text="Категория")
        self.stock_table.heading("Цена", text="Цена")
        self.stock_table.heading("Количество", text="Количество")
        self.stock_table.heading("Филиал", text="Филиал")
        self.stock_table.heading("Минимум", text="Минимум")
        self.stock_table.pack(fill="both", expand=True, padx=10, pady=10)

    def load_stock(self):
        """Загрузка остатков товаров из базы данных."""
        for row in self.stock_table.get_children():
            self.stock_table.delete(row)

        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM stock")
        stock = cursor.fetchall()

        for item in stock:
            self.stock_table.insert("", tk.END, values=item)

        # Проверяем на минимальный остаток
        self.check_min_stock(stock)

    def filter_stock(self):
        """Фильтрация товаров по заданным критериям."""
        category = self.category_filter.get()
        branch = self.branch_filter.get()
        name = self.name_filter.get()

        query = "SELECT * FROM stock WHERE 1=1"
        params = []

        if category != "Все":
            query += " AND category = ?"
            params.append(category)
        if branch != "Все":
            query += " AND branch LIKE ?"
            params.append(f"%{branch}%")
        if name != "Все":
            query += " AND name LIKE ?"
            params.append(f"%{name}%")

        cursor = self.db_connection.cursor()
        cursor.execute(query, params)
        filtered_stock = cursor.fetchall()

        # Обновляем таблицу
        for row in self.stock_table.get_children():
            self.stock_table.delete(row)

        for item in filtered_stock:
            self.stock_table.insert("", tk.END, values=item)

    def edit_stock(self):
        """Открыть окно для редактирования остатков."""
        selected_item = self.stock_table.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите товар для редактирования!")
            return

        item_id = self.stock_table.item(selected_item, "values")[0]

        # Окно редактирования
        edit_window = tk.Toplevel(self)
        edit_window.title("Редактирование остатков")
        edit_window.geometry("400x350")

        tk.Label(edit_window, text="Количество:").grid(row=0, column=0, padx=10, pady=10)
        quantity_entry = tk.Entry(edit_window)
        quantity_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Button(edit_window, text="Сохранить", command=lambda: self.save_stock(edit_window, item_id, quantity_entry.get(),)).grid(row=2, column=0, columnspan=2, pady=10)

    def save_stock(self, window, item_id, quantity):
        """Сохранение нового остатка в базе данных."""
        try:
            quantity = int(quantity)
            cursor = self.db_connection.cursor()
            if quantity == 0:
                cursor.execute("DELETE FROM stock WHERE id = ?", (item_id,))
            else:
                # Обновление количества товара
                cursor.execute("UPDATE stock SET quantity = ? WHERE id = ?", (quantity, item_id))

            self.db_connection.commit()
            window.destroy()
            self.load_stock()
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные данные!")

    def check_min_stock(self, stock):
        """Проверка на минимальные остатки."""
        for item in stock:
            try:
                quantity = int(item[4])
                minimum = int(item[6])
                if quantity < minimum:
                    messagebox.showwarning("Внимание", f"Товар '{item[1]}' в филиале '{item[5]}' достиг минимального остатка!")
            except ValueError:
                messagebox.showerror("Ошибка", "Неверные данные в базе!")

    def add_stock(self):
        """Открыть окно для добавления нового товара."""
        add_window = tk.Toplevel(self)
        add_window.title("Добавить новый товар")
        add_window.geometry("400x300")

        tk.Label(add_window, text="Название:").grid(row=0, column=0, padx=10, pady=10)
        name_entry = tk.Entry(add_window)
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(add_window, text="Категория:").grid(row=1, column=0, padx=10, pady=10)
        category_combo = ttk.Combobox(add_window, values=["Устройство", "Аксессуар", "SIM-карта"], state="readonly")
        category_combo.set("Устройство")
        category_combo.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(add_window, text="Количество:").grid(row=2, column=0, padx=10, pady=10)
        quantity_entry = tk.Entry(add_window)
        quantity_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(add_window, text="Филиал:").grid(row=3, column=0, padx=10, pady=10)
        branch_entry = tk.Entry(add_window)
        branch_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(add_window, text="Цена:").grid(row=4, column=0, padx=10, pady=10)
        price_entry = tk.Entry(add_window)
        price_entry.grid(row=4, column=1, padx=10, pady=10)

        tk.Button(
            add_window,
            text="Сохранить",
            command=lambda: self.save_new_stock(
                add_window,
                name_entry.get(),
                category_combo.get(),
                quantity_entry.get(),
                branch_entry.get(),
                price_entry.get()
            )
        ).grid(row=5, column=0, columnspan=2, pady=10)

    def save_new_stock(self, window, name, category, quantity, branch, price):
        """Сохранить новый товар в базе данных."""
        try:
            quantity = int(quantity)  # Приводим к целому числу
            price = float(price)  # Приводим к числу с плавающей запятой

            # Выполнение запроса
            cursor = self.db_connection.cursor()
            cursor.execute(
                "INSERT INTO stock (name, category, branch, quantity, price) VALUES (?, ?, ?, ?, ?)",
                (name, category, branch, quantity, price)
            )
            self.db_connection.commit()
            window.destroy()
            self.load_stock()
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные данные!")

    def get_branches(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT DISTINCT branch FROM stock")
        branches = cursor.fetchall()
        return [branch[0] for branch in branches]
    
    def get_names(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT DISTINCT name FROM stock")
        names = cursor.fetchall()
        return [name[0] for name in names]
    
    def refresh_tab(self):
        self.load_stock()
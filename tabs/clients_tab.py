import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog
import sqlite3
from datetime import datetime

class ClientsTab(tk.Frame):
    def __init__(self, parent, db_connection):
        super().__init__(parent)

        self.db_connection = db_connection
        self.parent = parent

        self.title_label = tk.Label(self, text="Учет клиентов", font=("Arial", 16))
        self.title_label.pack(pady=10)

        # Кнопка добавления нового клиента
        self.add_client_button = tk.Button(self, text="Добавить клиента", command=self.show_add_client_form)
        self.add_client_button.pack(pady=10)

        # Кнопка отображения истории покупок клиента
        self.show_history_button = tk.Button(self, text="История покупок клиента", command=self.show_client_history)
        self.show_history_button.pack(pady=10)

        # Таблица клиентов
        self.create_client_table()

    def create_client_table(self):
        """Создаем таблицу для отображения клиентов."""
        self.client_table = ttk.Treeview(self, columns=("ID", "Имя", "Фамилия", "Телефон", "Email", "Дата рождения", "Адрес"), show="headings")
        self.client_table.heading("ID", text="ID")
        self.client_table.heading("Имя", text="Имя")
        self.client_table.heading("Фамилия", text="Фамилия")
        self.client_table.heading("Телефон", text="Телефон")
        self.client_table.heading("Email", text="Email")
        self.client_table.heading("Дата рождения", text="Дата рождения")
        self.client_table.heading("Адрес", text="Адрес")
        self.client_table.pack(fill="both", expand=True, padx=10, pady=10)

        # Загружаем данные о клиентах
        self.load_clients()

    def load_clients(self):
        """Загружаем клиентов из базы данных."""
        for row in self.client_table.get_children():
            self.client_table.delete(row)

        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM clients")
        clients = cursor.fetchall()
        
        for client in clients:
            self.client_table.insert("", tk.END, values=client)

    def show_add_client_form(self):
        """Показываем форму для добавления нового клиента."""
        # Окно для ввода данных
        add_client_window = tk.Toplevel(self)
        add_client_window.title("Добавить клиента")
        add_client_window.geometry("400x300")

        # Поля для ввода
        tk.Label(add_client_window, text="Имя:").grid(row=0, column=0, pady=5, padx=5)
        self.first_name_entry = tk.Entry(add_client_window)
        self.first_name_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(add_client_window, text="Фамилия:").grid(row=1, column=0, pady=5, padx=5)
        self.last_name_entry = tk.Entry(add_client_window)
        self.last_name_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(add_client_window, text="Телефон:").grid(row=2, column=0, pady=5, padx=5)
        self.phone_entry = tk.Entry(add_client_window)
        self.phone_entry.grid(row=2, column=1, pady=5, padx=5)

        tk.Label(add_client_window, text="Email:").grid(row=3, column=0, pady=5, padx=5)
        self.email_entry = tk.Entry(add_client_window)
        self.email_entry.grid(row=3, column=1, pady=5, padx=5)

        tk.Label(add_client_window, text="Дата рождения:").grid(row=4, column=0, pady=5, padx=5)
        self.birth_date_entry = tk.Entry(add_client_window)
        self.birth_date_entry.grid(row=4, column=1, pady=5, padx=5)

        tk.Label(add_client_window, text="Адрес:").grid(row=5, column=0, pady=5, padx=5)
        self.address_entry = tk.Entry(add_client_window)
        self.address_entry.grid(row=5, column=1, pady=5, padx=5)

        # Кнопка сохранения данных
        save_button = tk.Button(add_client_window, text="Сохранить", command=lambda: self.save_client(add_client_window))
        save_button.grid(row=6, column=0, columnspan=2, pady=10)

    def save_client(self, window):
        """Сохраняем нового клиента в базе данных."""
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        birth_date = self.birth_date_entry.get()
        address = self.address_entry.get()

        # Проверка уникальности телефона и email
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM clients WHERE phone = ? OR email = ?", (phone, email))
        if cursor.fetchone()[0] > 0:
            messagebox.showerror("Ошибка", "Телефон или email уже существуют!")
            return

        # Вставляем данные в базу
        cursor.execute("""
            INSERT INTO clients (first_name, last_name, phone, email, birth_date, address)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (first_name, last_name, phone, email, birth_date, address))
        self.db_connection.commit()

        # Закрываем окно
        window.destroy()

        # Обновляем таблицу
        self.load_clients()

    def show_client_history(self):
        """Показываем историю покупок клиента."""
        # Получаем ID клиента
        selected_item = self.client_table.selection()

        if not selected_item:
            messagebox.showwarning("Ошибка", "Пожалуйста, выберите клиента из таблицы.")
            return

        # Получаем ID клиента из выбранной строки
        client_id = self.client_table.item(selected_item)["values"][0]

        cursor = self.db_connection.cursor()
        cursor.execute("""
            SELECT sales.sale_date, stock.name, sales.quantity, sales.unit_price, sales.total_price
            FROM sales
            JOIN stock ON sales.product_id = stock.id
            WHERE sales.client_id = ?
        """, (client_id,))
        
        sales = cursor.fetchall()

        if not sales:
            messagebox.showinfo("История покупок", "У этого клиента нет покупок.")
            return

        # Создаем новое окно для отображения истории
        history_window = tk.Toplevel(self)
        history_window.title("История покупок клиента")

        # Таблица для отображения покупок
        history_table = ttk.Treeview(history_window, columns=("Дата", "Товар", "Количество", "Цена за единицу", "Итоговая стоимость"), show="headings")
        history_table.heading("Дата", text="Дата")
        history_table.heading("Товар", text="Товар")
        history_table.heading("Количество", text="Количество")
        history_table.heading("Цена за единицу", text="Цена за единицу")
        history_table.heading("Итоговая стоимость", text="Итоговая стоимость")
        history_table.pack(fill="both", expand=True, padx=10, pady=10)

        for sale in sales:
            history_table.insert("", tk.END, values=sale)
    
    def refresh_tab(self):
        self.load_clients()


if __name__ == "__main__":
    root = tk.Tk()
    client_tab = ClientsTab(root, sqlite3.connect("salons.db"))
    client_tab.pack(fill="both", expand=True)
    root.mainloop()

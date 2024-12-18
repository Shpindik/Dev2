import tkinter as tk
from tkinter import ttk, messagebox


class SalesTab(tk.Frame):
    def __init__(self, parent, db_connection, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.db_connection = db_connection
        self.cursor = db_connection.cursor()

        self.branch_label = tk.Label(self, text="Выберите филиал:")
        self.branch_label.grid(row=0, column=0, padx=10, pady=10)

        self.branch_combobox = ttk.Combobox(self)
        self.branch_combobox.grid(row=0, column=1, padx=10, pady=10)
        self.load_branches()
        self.branch_combobox.bind("<<ComboboxSelected>>", self.load_products)

        self.product_label = tk.Label(self, text="Выберите товар:")
        self.product_label.grid(row=1, column=0, padx=10, pady=10)

        self.product_combobox = ttk.Combobox(self)
        self.product_combobox.grid(row=1, column=1, padx=10, pady=10)
        self.product_combobox.bind("<<ComboboxSelected>>",
                                   self.update_product_price)

        self.quantity_label = tk.Label(self, text="Количество:")
        self.quantity_label.grid(row=2, column=0, padx=10, pady=10)

        self.quantity_entry = tk.Entry(self)
        self.quantity_entry.grid(row=2, column=1, padx=10, pady=10)
        self.quantity_entry.bind("<KeyRelease>", self.calculate_total_price)

        self.unit_price_label = tk.Label(self, text="Цена за единицу:")
        self.unit_price_label.grid(row=3, column=0, padx=10, pady=10)

        self.unit_price_entry = tk.Entry(self, state="readonly")
        self.unit_price_entry.grid(row=3, column=1, padx=10, pady=10)

        self.discount_label = tk.Label(self, text="Скидка (Сумма):")
        self.discount_label.grid(row=4, column=0, padx=10, pady=10)

        self.discount_entry = tk.Entry(self)
        self.discount_entry.grid(row=4, column=1, padx=10, pady=10)
        self.discount_entry.bind("<KeyRelease>", self.calculate_total_price)

        self.total_price_label = tk.Label(self, text="Итоговая стоимость:")
        self.total_price_label.grid(row=5, column=0, padx=10, pady=10)

        self.total_price_entry = tk.Entry(self, state="readonly")
        self.total_price_entry.grid(row=5, column=1, padx=10, pady=10)

        self.client_label = tk.Label(self, text="Выберите клиента:")
        self.client_label.grid(row=6, column=0, padx=10, pady=10)

        self.client_combobox = ttk.Combobox(self)
        self.client_combobox.grid(row=6, column=1, padx=10, pady=10)
        self.load_clients()

        self.save_button = tk.Button(
            self,
            text="Сохранить продажу",
            command=self.save_sale)
        self.save_button.grid(row=7, column=0, columnspan=2, pady=20)

    def load_branches(self):
        """Загрузка филиалов из базы данных."""
        self.cursor.execute("SELECT DISTINCT branch FROM stock")
        branches = [row[0] for row in self.cursor.fetchall()]
        self.branch_combobox['values'] = branches

    def load_products(self, event=None):
        """Загрузка товаров из выбранного филиала."""
        selected_branch = self.branch_combobox.get()
        if not selected_branch:
            return

        self.cursor.execute("SELECT id, name, price, quantity \
                            FROM stock WHERE branch = ?", (selected_branch,))
        products = self.cursor.fetchall()
        product_names = [product[1] for product in products]
        self.product_combobox['values'] = product_names
        self.products_data = {
            product[1]: {
                'id': product[0],
                'price': product[2],
                'quantity': product[3]
            } for product in products
        }

    def update_product_price(self, event=None):
        """Обновление цены и проверки наличия товара при выборе."""
        selected_product = self.product_combobox.get()
        if selected_product in self.products_data:
            product_data = self.products_data[selected_product]
            self.unit_price_entry.config(state="normal")
            self.unit_price_entry.delete(0, tk.END)
            self.unit_price_entry.insert(0, product_data['price'])
            self.unit_price_entry.config(state="readonly")
            self.calculate_total_price()

    def load_clients(self):
        """Загрузка клиентов из базы данных для выбора."""
        self.cursor.execute("SELECT id, first_name, last_name FROM clients")
        clients = self.cursor.fetchall()
        client_names = [f"{client[1]} {client[2]}" for client in clients]
        self.client_combobox['values'] = client_names
        self.clients_data = {
            f"{client[1]} {client[2]}": client[0] for client in clients
        }

    def calculate_total_price(self, event=None):
        """Расчет итоговой стоимости с учетом скидки."""
        try:
            quantity = int(self.quantity_entry.get()) \
                if self.quantity_entry.get() else 0
            unit_price = float(self.unit_price_entry.get()) \
                if self.unit_price_entry.get() else 0
            discount = float(self.discount_entry.get()) \
                if self.discount_entry.get() else 0
            total_price = (quantity * unit_price) - discount
            self.total_price_entry.config(state="normal")
            self.total_price_entry.delete(0, tk.END)
            self.total_price_entry.insert(0, f"{total_price:.2f}")
            self.total_price_entry.config(state="readonly")
        except ValueError:
            self.total_price_entry.config(state="normal")
            self.total_price_entry.delete(0, tk.END)
            self.total_price_entry.config(state="readonly")

    def save_sale(self):
        """Сохранение данных о продаже в базу данных."""
        try:
            selected_branch = self.branch_combobox.get()
            selected_product = self.product_combobox.get()
            product_data = self.products_data[selected_product]
            quantity = int(self.quantity_entry.get())
            if quantity > product_data['quantity']:
                messagebox.showerror(
                    "Ошибка", "Недостаточно товара на складе."
                )
                return
            unit_price = float(self.unit_price_entry.get())
            discount = float(self.discount_entry.get()) \
                if self.discount_entry.get() else 0
            total_price = float(self.total_price_entry.get())
            selected_client = self.client_combobox.get()
            client_id = self.clients_data[selected_client]

            self.cursor.execute('''
                INSERT INTO sales (product_id, client_id, quantity, \
                                unit_price, discount, total_price, branch)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (product_data['id'], client_id, quantity, unit_price,
                  discount, total_price, selected_branch))
            self.db_connection.commit()

            self.cursor.execute('''
                UPDATE stock SET quantity = quantity - ? WHERE id = ?
            ''', (quantity, product_data['id']))
            self.db_connection.commit()

            self.load_products()
            messagebox.showinfo("Успех", "Продажа сохранена успешно!")
        except Exception as e:
            messagebox.showerror(
                "Ошибка", f"Ошибка при сохранении продажи: {e}"
            )

    def refresh_tab(self):
        """Обновление данных вкладки."""
        self.load_branches()
        if self.branch_combobox.get():
            self.load_products()
        self.load_clients()

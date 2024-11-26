import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class StockFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#ffffff")

        tk.Label(self, text="Учет остатков товаров", font=("Arial", 16, "bold"), bg="#ffffff").pack(pady=10)

        # Таблица с данными
        columns = ["Товар", "Категория", "Количество", "Филиал"]
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)

        for col in columns:
            self.tree.heading(col, text=col, command=lambda _col=col: self.sort_column(_col, False))
            self.tree.column(col, anchor="center")

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Прокрутка
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Управляющие кнопки
        button_frame = tk.Frame(self, bg="#ffffff")
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Добавить товар", command=self.add_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Редактировать", command=self.edit_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Удалить", command=self.delete_item).pack(side=tk.LEFT, padx=5)

    def sort_column(self, col, reverse):
        """Сортировка таблицы"""
        data = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        data.sort(reverse=reverse)
        for index, (_, k) in enumerate(data):
            self.tree.move(k, "", index)
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))

    def add_item(self):
        messagebox.showinfo("Добавление", "Добавление товара")

    def edit_item(self):
        messagebox.showinfo("Редактирование", "Редактирование товара")

    def delete_item(self):
        messagebox.showinfo("Удаление", "Удаление товара")

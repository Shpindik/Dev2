import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
import sqlite3
import os

from tabs.sales_tab import SalesTab
from tabs.clients_tab import ClientsTab
from tabs.stock_tab import StockTab
from tabs.report_tab import ReportTab


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Информационная система для сети салонов связи")
        self.geometry("1200x800")

        # Соединение с базой данных
        self.db_connection = sqlite3.connect("salons.db")
        
        # Главное меню
        self.create_menu()

        # Вкладки
        self.create_tabs()

        # Кнопка "О приложении" внизу
        self.create_about_button()

    def create_menu(self):
        """Создание главного меню."""
        menu = tk.Menu(self)
        self.config(menu=menu)

        # Меню "Файл"
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Выход", command=self.quit)

        # Меню "Помощь"
        help_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Помощь", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)

    def create_tabs(self):
        """Создание вкладок для навигации."""
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        # Вкладка Учет продаж
        sales_tab = SalesTab(notebook, self.db_connection)
        notebook.add(sales_tab, text="Учет продаж")

        # Вкладка Клиенты (будем добавлять позже)
        clients_tab = ClientsTab(notebook, self.db_connection)
        notebook.add(clients_tab, text="Клиенты")

        # Вкладка Склад (будем добавлять позже)
        stock_tab = StockTab(notebook, self.db_connection)
        notebook.add(stock_tab, text="Склад")

        # Вкладка Отчеты (будем добавлять позже)
        reports_tab = ReportTab(notebook, self.db_connection)
        notebook.add(reports_tab, text="Отчеты")

    def create_about_button(self):
        """Создание кнопки 'О приложении' внизу."""
        about_button = tk.Button(self, text="О приложении", command=self.show_about_window)
        about_button.pack(side="bottom", pady=10)

    def show_about(self):
        """Показать информацию о программе."""
        messagebox.showinfo("О программе", "Информационная система для сети салонов связи\nВерсия 1.0")

    def show_about_window(self):
        """Открытие окна с информацией из about.txt."""
        # Путь к файлу about.txt
        file_path = os.path.join(os.path.dirname(__file__), "about.txt")

        # Проверяем, существует ли файл
        if os.path.exists(file_path):
            # Читаем содержимое файла
            with open(file_path, "r", encoding="utf-8") as file:
                about_content = file.read()

            # Создаем новое окно для отображения информации
            about_window = tk.Toplevel(self)
            about_window.title("О приложении")
            about_window.geometry("400x300")

            # Используем scrolledtext для отображения большого текста
            text_area = scrolledtext.ScrolledText(about_window, wrap=tk.WORD, width=45, height=10)
            text_area.pack(padx=10, pady=10)
            text_area.insert(tk.END, about_content)
            text_area.config(state=tk.DISABLED)  # Делаем текст только для чтения
        else:
            messagebox.showerror("Ошибка", "Файл about.txt не найден!")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
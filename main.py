import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import os
import subprocess

from tabs.sales_tab import SalesTab
from tabs.clients_tab import ClientsTab
from tabs.stock_tab import StockTab
from tabs.report_tab import ReportTab


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Информационная система для сети салонов связи")
        self.geometry("1200x800")

        # Запуск database.py для генерации базы данных
        self.run_database_script()

        # Соединение с базой данных
        self.db_connection = sqlite3.connect("salons.db")
        
        # Главное меню
        self.create_menu()

        # Вкладки
        self.create_tabs()

        # Кнопка "О приложении" внизу
        self.create_about_button()

        # Переопределение метода закрытия приложения
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def run_database_script(self):
        """Запуск database.py для создания базы данных."""
        try:
            subprocess.run(["python", "database.py"], check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Ошибка", f"Ошибка при создании базы данных: {e}")
            self.destroy()

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
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Вкладка Учет продаж
        self.sales_tab = SalesTab(self.notebook, self.db_connection)
        self.notebook.add(self.sales_tab, text="Учет продаж")

        # Вкладка Клиенты
        self.clients_tab = ClientsTab(self.notebook, self.db_connection)
        self.notebook.add(self.clients_tab, text="Клиенты")

        # Вкладка Склад
        self.stock_tab = StockTab(self.notebook, self.db_connection)
        self.notebook.add(self.stock_tab, text="Склад")

        # Вкладка Отчеты
        self.reports_tab = ReportTab(self.notebook, self.db_connection)
        self.notebook.add(self.reports_tab, text="Отчеты")

        # Привязка события смены вкладки
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def on_tab_change(self, event):
        """Обработчик смены вкладки."""
        selected_tab = event.widget.tab(event.widget.index("current"))["text"]

        if selected_tab == "Учет продаж":
            self.sales_tab.refresh_tab()
        elif selected_tab == "Клиенты":
            self.clients_tab.refresh_tab()
        elif selected_tab == "Склад":
            self.stock_tab.refresh_tab()
        elif selected_tab == "Отчеты":
            self.reports_tab.refresh_tab()

    def create_about_button(self):
        """Создание кнопки 'О приложении' внизу."""
        about_button = tk.Button(self, text="О приложении", command=self.show_about_window)
        about_button.pack(side="bottom", pady=10)

    def show_about(self):
        """Показать информацию о программе."""
        messagebox.showinfo("О программе", "Информационная система для сети салонов связи\nВерсия 1.0")

    def show_about_window(self):
        """Открытие окна с информацией из about.txt."""
        file_path = os.path.join(os.path.dirname(__file__), "about.txt")

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                about_content = file.read()

            about_window = tk.Toplevel(self)
            about_window.title("О приложении")
            about_window.geometry("400x300")

            text_area = tk.Text(about_window, wrap=tk.WORD, width=45, height=10)
            text_area.pack(padx=10, pady=10)
            text_area.insert(tk.END, about_content)
            text_area.config(state=tk.DISABLED)
        else:
            messagebox.showerror("Ошибка", "Файл about.txt не найден!")

    def on_close(self):
        """Действия при закрытии приложения."""
        if messagebox.askokcancel("Выход", "Вы действительно хотите выйти?"):
            self.cleanup_database()
            self.destroy()

    def cleanup_database(self):
        """Удаление базы данных при выходе."""
        self.db_connection.close()
        if os.path.exists("salons.db"):
            os.remove("salons.db")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

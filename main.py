import tkinter as tk
from frames.sales import SalesFrame
from frames.clients import ClientsFrame
from frames.stock import StockFrame
from frames.reports import ReportsFrame


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Информационная система сети салонов связи")
        self.geometry("900x600")
        self.configure(bg="#f4f4f4")

        # Верхнее меню
        menu = tk.Menu(self)
        self.config(menu=menu)

        menu.add_command(label="Продажи", command=self.show_sales)
        menu.add_command(label="Клиенты", command=self.show_clients)
        menu.add_command(label="Склад", command=self.show_stock)
        menu.add_command(label="Отчеты", command=self.show_reports)

        # Каркас для разделов
        self.frames = {}
        for F in (SalesFrame, ClientsFrame, StockFrame, ReportsFrame):
            frame = F(self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_sales()

    def show_frame(self, name):
        """Отображение выбранного раздела"""
        frame = self.frames[name]
        frame.tkraise()

    def show_sales(self):
        self.show_frame("SalesFrame")

    def show_clients(self):
        self.show_frame("ClientsFrame")

    def show_stock(self):
        self.show_frame("StockFrame")

    def show_reports(self):
        self.show_frame("ReportsFrame")


if __name__ == "__main__":
    app = App()
    app.mainloop()

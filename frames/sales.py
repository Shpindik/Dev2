import tkinter as tk


class SalesFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#ffffff")
        tk.Label(self, text="Раздел: Продажи", font=("Arial", 16), bg="#ffffff").pack(pady=10)
        # Элементы интерфейса для продаж

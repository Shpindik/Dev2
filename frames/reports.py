import tkinter as tk


class ReportsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#ffffff")
        tk.Label(self, text="Раздел: Отчеты", font=("Arial", 16), bg="#ffffff").pack(pady=10)
        # Элементы интерфейса для отчетов

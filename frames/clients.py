import tkinter as tk


class ClientsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#ffffff")
        tk.Label(self, text="Раздел: Клиенты", font=("Arial", 16), bg="#ffffff").pack(pady=10)
        # Элементы интерфейса для клиентов

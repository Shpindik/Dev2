import os
from tkinter import filedialog
from tkinter import messagebox, ttk
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime, timedelta


class ReportTab(ttk.Frame):
    def __init__(self, parent, db_connection, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.db_connection = db_connection
        self.cursor = db_connection.cursor()

        # Интерфейс
        self.setup_ui()

    def setup_ui(self):
        """Создание кнопок и интерфейса для отчетов."""
        ttk.Label(self, text="Отчеты", font=("Helvetica", 16)).pack(pady=10)

        ttk.Button(self, text="Отчет по продажам (день)", command=lambda: self.generate_sales_report("day")).pack(pady=5)
        ttk.Button(self, text="Отчет по продажам (неделя)", command=lambda: self.generate_sales_report("week")).pack(pady=5)
        ttk.Button(self, text="Популярные товары", command=self.generate_popular_products_report).pack(pady=5)
        ttk.Button(self, text="Экспортировать в Excel", command=self.export_to_excel).pack(pady=5)
        ttk.Button(self, text="Экспортировать в PDF", command=self.export_to_pdf).pack(pady=5)

    def generate_sales_report(self, period="day"):
        """Генерация отчета по продажам за указанный период."""
        # Определение диапазона дат
        if period == "day":
            start_date = datetime.now() - timedelta(days=1)
        elif period == "week":
            start_date = datetime.now() - timedelta(weeks=1)
        else:
            start_date = None

        start_date_str = start_date.strftime('%Y-%m-%d %H:%M:%S') if start_date else None

        # SQL запрос
        query = '''
            SELECT p.name, s.quantity, s.unit_price, s.discount, s.total_price, s.sale_date
            FROM sales s
            JOIN stock p ON s.product_id = p.id
            WHERE s.sale_date >= ?
            ORDER BY s.sale_date DESC
        '''
        self.cursor.execute(query, (start_date_str,))
        sales_data = self.cursor.fetchall()

        # Итоги
        total_sales = sum(item[4] for item in sales_data)
        total_quantity = sum(item[1] for item in sales_data)
        profit = sum((item[2] - item[3]) * item[1] for item in sales_data)

        messagebox.showinfo(
            "Отчет по продажам",
            f"Общая сумма: {total_sales}\nОбщее количество: {total_quantity}\nПрибыль: {profit}"
        )

    def generate_popular_products_report(self):
        """Генерация отчета по популярным товарам."""
        query = '''
            SELECT p.name, SUM(s.quantity) AS total_sales
            FROM sales s
            JOIN stock p ON s.product_id = p.id
            GROUP BY p.name
            ORDER BY total_sales DESC
        '''
        self.cursor.execute(query)
        popular_products = self.cursor.fetchall()

        message = "\n".join([f"{name}: {total_sales} продаж" for name, total_sales in popular_products])
        messagebox.showinfo("Популярные товары", message)

    def export_to_excel(self):
        """Экспорт отчета в Excel."""
        # Получить путь для сохранения файла
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
            title="Сохранить как"
        )
        if not file_path:
            return

        query = '''
            SELECT p.name, s.quantity, s.unit_price, s.discount, s.total_price, s.sale_date
            FROM sales s
            JOIN stock p ON s.product_id = p.id
            ORDER BY s.sale_date DESC
        '''
        self.cursor.execute(query)
        sales_data = self.cursor.fetchall()

        wb = Workbook()
        ws = wb.active
        ws.title = "Sales Report"

        # Заголовки
        ws.append(["Product", "Quantity", "Unit Price", "Discount", "Total Price", "Sale Date"])

        # Данные
        for row in sales_data:
            ws.append(row)

        wb.save(file_path)
        messagebox.showinfo("Экспорт", f"Отчет успешно сохранен: {file_path}")

    def export_to_pdf(self):
        """Экспорт отчета в PDF."""
        # Получить путь для сохранения файла
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Сохранить как"
        )
        if not file_path:
            return

        query = '''
            SELECT p.name, s.quantity, s.unit_price, s.discount, s.total_price, s.sale_date
            FROM sales s
            JOIN stock p ON s.product_id = p.id
            ORDER BY s.sale_date DESC
        '''
        self.cursor.execute(query)
        sales_data = self.cursor.fetchall()

        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica", 12)
        c.drawString(100, height - 50, "Sales Report")

        # Заголовки
        c.drawString(100, height - 80, "Product")
        c.drawString(250, height - 80, "Quantity")
        c.drawString(350, height - 80, "Total Price")

        y = height - 100
        for row in sales_data:
            c.drawString(100, y, row[0])  # Product name
            c.drawString(250, y, str(row[1]))  # Quantity
            c.drawString(350, y, str(row[4]))  # Total Price
            y -= 20
            if y < 50:  # Переход на новую страницу
                c.showPage()
                c.setFont("Helvetica", 12)
                y = height - 50

        c.save()
        messagebox.showinfo("Экспорт", f"Отчет успешно сохранен: {file_path}")
    
    def refresh_tab(self):
        self.generate_sales_report()

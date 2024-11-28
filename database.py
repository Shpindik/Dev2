import random
import sqlite3

from faker import Faker

conn = sqlite3.connect("salons.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE,
    birth_date DATE,
    address TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    client_id INTEGER,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    discount REAL DEFAULT 0,
    total_price REAL NOT NULL,
    branch TEXT NOT NULL,
    sale_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products (id),
    FOREIGN KEY (client_id) REFERENCES clients (id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS stock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL CHECK (category IN ('Устройство', \
               'Аксессуар', 'SIM-карта')),
    price INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0,
    branch TEXT NOT NULL,
    min_quantity INTEGER DEFAULT 10
);
''')

conn.commit()
conn.close()

faker = Faker("ru_RU")

conn = sqlite3.connect("salons.db")
cursor = conn.cursor()


def populate_clients():
    """Создает от 5 до 10 случайных клиентов с проверкой уникальности."""
    num_clients = random.randint(5, 10)
    clients = []
    for _ in range(num_clients):
        gender = random.choice(['male', 'female'])
        if gender == 'male':
            first_name = faker.first_name_male()
            last_name = faker.last_name_male()
        else:
            first_name = faker.first_name_female()
            last_name = faker.last_name_female()
        while True:
            phone = faker.phone_number()
            email = faker.unique.email()
            cursor.execute("SELECT * FROM clients WHERE phone = ? \
                           OR email = ?", (phone, email))
            if not cursor.fetchone():
                break
        birth_date = faker.date_of_birth(minimum_age=18,
                                         maximum_age=70).strftime('%Y-%m-%d')
        address = faker.address()
        clients.append((
            first_name,
            last_name,
            phone,
            email,
            birth_date,
            address
        ))
    cursor.executemany('''
        INSERT INTO clients (first_name, last_name, phone, \
                       email, birth_date, address)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', clients)


def populate_stock():
    """Создает позиции для разных категорий на складе."""
    accessories = [
        "AirPods",
        "AirPods Pro",
        "Galaxy Buds",
        "JBL Clip",
        "Sony WH-1000XM5"
    ]
    sim_cards = [
        "Сим-карта МТС",
        "Сим-карта Билайн",
        "Сим-карта Йота",
        "Сим-карта Tele2",
        "Сим-карта Мегафон"
    ]
    devices = [
        "iPhone 15",
        "Google Pixel 8",
        "Samsung Galaxy S23",
        "OnePlus 12",
        "Xiaomi 13"
    ]
    categories = {
        'Аксессуар': accessories,
        'SIM-карта': sim_cards,
        'Устройство': devices
    }
    branches = ['Москва', 'Санкт-Петербург', 'Новосибирск']
    num_products = random.randint(10, 20)
    stock = []
    for _ in range(num_products):
        category = random.choice(list(categories.keys()))
        name = random.choice(categories[category])
        price = random.randint(500, 50000)
        quantity = random.randint(1, 100)
        branch = random.choice(branches)
        min_quantity = random.randint(5, 15)
        stock.append((name, category, price, quantity, branch, min_quantity))
    cursor.executemany('''
        INSERT INTO stock (name, category, price, quantity, \
                       branch, min_quantity)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', stock)


def populate_database():
    try:
        populate_clients()
        populate_stock()
        conn.commit()
        print("База данных успешно заполнена.")
    except sqlite3.IntegrityError as e:
        print("Ошибка уникальности:", e)


populate_database()

# Закрытие соединения
conn.close()

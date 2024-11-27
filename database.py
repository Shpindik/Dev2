import sqlite3

# Создание базы данных
conn = sqlite3.connect("salons.db")
cursor = conn.cursor()

# Таблица клиентов
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

# Таблица продаж
cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    client_id INTEGER,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    discount REAL DEFAULT 0,
    total_price REAL NOT NULL,
    sale_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products (id),
    FOREIGN KEY (client_id) REFERENCES clients (id)
)
''')

# Таблица остатков
cursor.execute('''
CREATE TABLE IF NOT EXISTS stock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL CHECK (category IN ('Устройство', 'Аксессуар', 'SIM-карта')),
    price INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0,
    branch TEXT NOT NULL,
    min_quantity INTEGER DEFAULT 10
);
''')

conn.commit()
conn.close()

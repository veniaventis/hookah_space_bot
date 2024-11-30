import sqlite3


# Устанавливаем соединение с базой данных
def create_connection():
    connection = sqlite3.connect("orders.db")  # Имя файла базы данных
    return connection


# Создаем таблицы (запускается один раз при старте приложения)
def initialize_database():
    connection = create_connection()
    cursor = connection.cursor()

    # Таблица для хранения заказов
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hookah TEXT NOT NULL,           -- Тип кальяна
            price REAL NOT NULL,            -- Цена
            payment TEXT NOT NULL,          -- Тип оплаты
            admin_id INTEGER NOT NULL,      -- ID администратора
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP -- Время создания заказа
        )
    """)

    connection.commit()
    connection.close()


def save_order(hookah, price, payment, admin_id):
    connection = create_connection()
    cursor = connection.cursor()

    # Запись данных о заказе
    cursor.execute("""
        INSERT INTO orders (hookah, price, payment, admin_id)
        VALUES (?, ?, ?, ?)
    """, (hookah, price, payment, admin_id))

    connection.commit()
    connection.close()


def get_shift_stats(admin_id="5477880310,1614891721"):
    connection = create_connection()
    cursor = connection.cursor()

    # Выборка данных по текущей дате
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN payment = 'pay_cash' THEN price ELSE 0 END) AS cash,
            SUM(CASE WHEN payment = 'pay_card' THEN price ELSE 0 END) AS card,
            SUM(CASE WHEN payment = 'bonus' THEN price ELSE 0 END) AS bonus
        FROM orders
        WHERE admin_id = ? AND DATE(timestamp) = DATE('now')
    """, (admin_id,))

    result = cursor.fetchone()
    connection.close()

    return {
        "cash": result[0] or 0,
        "card": result[1] or 0,
        "bonus": result[2] or 0
    }


"""Модуль для работы с заказами (Интеграция)."""
import sqlite3
from datetime import datetime
from config import DB_PATH

def get_connection():
    """Возвращает соединение с БД."""
    return sqlite3.connect(DB_PATH)

def add_order_to_db(client, product_id, quantity):
    """
    Добавляет новый заказ в таблицу 'Заказ'.
    Возвращает id созданного заказа.
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # Получаем текущую дату в формате YYYY-MM-DD
    date = datetime.now().strftime("%Y-%m-%d")
    
    # Вставляем запись в таблицу Заказ
    # Поля: дата, клиент, товар_id, количество
    cur.execute(
        "INSERT INTO Заказ (дата, клиент, товар_id, количество) VALUES (?, ?, ?, ?)",
        (date, client, product_id, quantity)
    )
    
    conn.commit()
    order_id = cur.lastrowid  # Получаем ID только что созданного заказа
    conn.close()
    
    return order_id

def update_product_quantity(product_id, new_quantity):
    """
    Обновляет количество мест в таблице 'Товар'.
    """
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute(
        "UPDATE Товар SET количество = ? WHERE id = ?",
        (new_quantity, product_id)
    )
    
    conn.commit()
    conn.close()

def get_product_quantity(product_id):
    """
    Возвращает текущее количество мест для товара.
    """
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()
    
    return row[0] if row else 0
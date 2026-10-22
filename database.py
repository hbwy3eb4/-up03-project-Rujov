"""Модуль для работы с базой данных."""
import sqlite3

DB_PATH = "databases/db_variant_12.db"

def get_all_products():
    """Возвращает список всех туров из БД."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        # Порядок полей: 0=id, 1=страна, 2=город, 3=длительность, 4=цена, 5=количество, 6=фото
        cur.execute("SELECT * FROM Товар ORDER BY id")
        products = cur.fetchall()
        conn.close()
        return products
    except sqlite3.Error as e:
        print(f"Ошибка БД: {e}")
        return []
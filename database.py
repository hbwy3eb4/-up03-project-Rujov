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
def get_user_by_login(login):
    """
    Ищет пользователя по логину.
    :param login: логин
    :return: кортеж (id, фамилия, имя, отчество, логин, роль) или None
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT Пользователь.id, Пользователь.фамилия,
               Пользователь.имя, Пользователь.отчество,
               Пользователь.логин, Роль.название
        FROM Пользователь
        JOIN Роль ON Пользователь.роль_id = Роль.id
        WHERE Пользователь.логин = ?
    """, (login,))
    row = cur.fetchone()
    conn.close()
    return row
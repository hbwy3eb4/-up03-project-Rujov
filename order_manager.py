"""Модуль для работы с заказами (Пары 22-27)."""
import sqlite3
from datetime import datetime
from config import DB_PATH


def get_connection():
    """Возвращает соединение с БД."""
    return sqlite3.connect(DB_PATH)


def get_product_quantity(product_id):
    """Возвращает текущее количество мест для товара."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0


def update_product_quantity(product_id, new_quantity):
    """Обновляет количество товара в БД."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE Товар SET количество = ? WHERE id = ?",
            (new_quantity, product_id)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Ошибка обновления количества: {e}")
    finally:
        conn.close()


def add_order_to_db(client, product_id, quantity):
    """
    Добавляет новый заказ в БД (для обратной совместимости).
    :param client: ФИО клиента
    :param product_id: id товара
    :param quantity: количество
    :return: id заказа или None при ошибке
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        date = datetime.now().strftime("%Y-%m-%d")
        cur.execute(
            "INSERT INTO Заказ (дата, клиент) VALUES (?, ?)",
            (date, client)
        )
        order_id = cur.lastrowid
        
        # Получаем цену товара
        cur.execute("SELECT цена FROM Товар WHERE id = ?", (product_id,))
        row = cur.fetchone()
        price = row[0] if row else 0.0
        
        # Добавляем позицию в состав заказа
        cur.execute(
            "INSERT INTO Состав_заказа (заказ_id, товар_id, количество, цена) "
            "VALUES (?, ?, ?, ?)",
            (order_id, product_id, quantity, price)
        )
        
        # Уменьшаем количество мест
        cur.execute(
            "UPDATE Товар SET количество = количество - ? WHERE id = ?",
            (quantity, product_id)
        )
        
        conn.commit()
        return order_id
    except Exception as e:
        conn.rollback()
        print(f"Ошибка добавления заказа: {e}")
        return None
    finally:
        conn.close()


def create_order(client, items):
    """
    Создаёт заказ с несколькими позициями (Транзакция).
    :param client: ФИО клиента
    :param items: список кортежей [(product_id, quantity, price), ...]
    :return: id заказа или None при ошибке
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        # 1. Создаём сам заказ
        date = datetime.now().strftime("%Y-%m-%d")
        cur.execute(
            "INSERT INTO Заказ (дата, клиент) VALUES (?, ?)",
            (date, client)
        )
        order_id = cur.lastrowid
        
        # 2. Добавляем позиции в Состав_заказа и уменьшаем остатки
        for product_id, quantity, price in items:
            # Проверяем наличие мест
            cur.execute(
                "SELECT количество FROM Товар WHERE id = ?",
                (product_id,)
            )
            row = cur.fetchone()
            
            if not row or row[0] < quantity:
                raise ValueError(
                    f"Недостаточно мест для тура (ID: {product_id}). "
                    f"Доступно: {row[0] if row else 0}"
                )
            
            # Добавляем в состав заказа
            cur.execute(
                "INSERT INTO Состав_заказа "
                "(заказ_id, товар_id, количество, цена) "
                "VALUES (?, ?, ?, ?)",
                (order_id, product_id, quantity, price)
            )
            
            # Уменьшаем количество мест в таблице Товар
            cur.execute(
                "UPDATE Товар SET количество = количество - ? WHERE id = ?",
                (quantity, product_id)
            )
        
        # 3. Если всё прошло успешно, фиксируем изменения
        conn.commit()
        return order_id
    except Exception as e:
        # 4. Если произошла любая ошибка, отменяем ВСЕ изменения
        conn.rollback()
        print(f"Ошибка создания заказа (откат транзакции): {e}")
        return None
    finally:
        conn.close()


def get_all_orders():
    """
    Возвращает список всех заказов.
    :return: список кортежей (id, дата, клиент)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, дата, клиент FROM Заказ ORDER BY id DESC"
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def get_order_by_id(order_id):
    """
    Возвращает заказ по id.
    :param order_id: id заказа
    :return: кортеж (id, дата, клиент) или None
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, дата, клиент FROM Заказ WHERE id = ?",
        (order_id,)
    )
    row = cur.fetchone()
    conn.close()
    return row


def get_order_items(order_id):
    """
    Возвращает состав заказа с полной информацией (JOIN).
    :param order_id: id заказа
    :return: список кортежей (id, страна, город, количество, цена)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT Состав_заказа.id,
               Товар.страна,
               Товар.город,
               Состав_заказа.количество,
               Состав_заказа.цена
        FROM Состав_заказа
        JOIN Товар ON Состав_заказа.товар_id = Товар.id
        WHERE Состав_заказа.заказ_id = ?
        ORDER BY Состав_заказа.id
        """,
        (order_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def get_order_total(order_id):
    """
    Возвращает итоговую сумму заказа.
    :param order_id: id заказа
    :return: сумма (float)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT SUM(количество * цена)
        FROM Состав_заказа
        WHERE заказ_id = ?
        """,
        (order_id,)
    )
    row = cur.fetchone()
    conn.close()
    return row[0] if row and row[0] else 0.0


def update_order_date(order_id, new_date):
    """
    Обновляет дату заказа.
    :param order_id: id заказа
    :param new_date: новая дата в формате YYYY-MM-DD
    :return: True при успехе, False при ошибке
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE Заказ SET дата = ? WHERE id = ?",
            (new_date, order_id)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Ошибка обновления даты: {e}")
        return False
    finally:
        conn.close()


def delete_order_item(item_id):
    """
    Удаляет позицию из состава заказа и восстанавливает остатки товара.
    :param item_id: id позиции в Состав_заказа
    :return: True при успехе, False при ошибке
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        # 1. Получаем данные позиции, чтобы знать, что возвращать на склад
        cur.execute(
            "SELECT товар_id, количество FROM Состав_заказа WHERE id = ?",
            (item_id,)
        )
        row = cur.fetchone()
        if not row:
            return False
        
        product_id, quantity = row
        
        # 2. Удаляем позицию из состава заказа
        cur.execute(
            "DELETE FROM Состав_заказа WHERE id = ?",
            (item_id,)
        )
        
        # 3. Восстанавливаем количество мест в таблице Товар
        cur.execute(
            "UPDATE Товар SET количество = количество + ? WHERE id = ?",
            (quantity, product_id)
        )
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Ошибка удаления позиции: {e}")
        return False
    finally:
        conn.close()
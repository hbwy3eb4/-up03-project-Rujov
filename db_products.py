"""Загрузка туров из БД в объекты класса Product с расширенным выводом."""
import sqlite3
from config import DB_PATH
from models import Product

def get_all_products():
    """Возвращает список всех объектов Product из БД."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    
    products = []
    for row in rows:
        product = Product(
            product_id=row[0],
            country=row[1],
            city=row[2],
            duration=row[3],
            price=row[4],
            quantity=row[5],
            photo=row[6]
        )
        products.append(product)
    return products

def get_products_by_country(country):
    """Возвращает список объектов Product по стране."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE страна = ?", (country,))
    rows = cur.fetchall()
    conn.close()
    
    products = []
    for row in rows:
        product = Product(
            product_id=row[0],
            country=row[1],
            city=row[2],
            duration=row[3],
            price=row[4],
            quantity=row[5],
            photo=row[6]
        )
        products.append(product)
    return products

def get_products_low_stock():
    """Возвращает товары с количеством мест <= 5 (или <= 3, как в задании)."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE количество <= 5")
    rows = cur.fetchall()
    conn.close()
    
    products = []
    for row in rows:
        product = Product(
            product_id=row[0],
            country=row[1],
            city=row[2],
            duration=row[3],
            price=row[4],
            quantity=row[5],
            photo=row[6]
        )
        products.append(product)
    return products

def print_catalog_with_highlight(products, title):
    """Выводит каталог с подсветкой для товаров с низким остатком."""
    print(f"\n{'=' * 80}")
    print(f" {title} ({len(products)} туров)")
    print("=" * 80)
    for p in products:
        # Подсветка ⚠️, если количество мест <= 5 (совпадает с логикой indicator "мало")
        highlight = " ⚠️ " if p.quantity <= 5 else "    "
        print(f"{highlight} {p.info()}")
    print("=" * 80)

if __name__ == "__main__":
    # 1. Все туры
    all_products = get_all_products()
    print_catalog_with_highlight(all_products, "КАТАЛОГ ВСЕХ ТУРОВ")
    
    # 2. Туры в конкретную страну (например, "Турция" или "Египет")
    turkey_products = get_products_by_country("Турция")
    print_catalog_with_highlight(turkey_products, "ТУРЫ В ТУРЦИЮ")
    
    # 3. Туры с низким остатком мест (<= 5)
    low_stock_products = get_products_low_stock()
    print_catalog_with_highlight(low_stock_products, "ТУРЫ С НИЗКИМ ОСТАТКОМ МЕСТ (<= 5)")
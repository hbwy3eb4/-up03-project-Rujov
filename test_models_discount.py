"""Проверка метода price_with_discount_auto в классе Product."""
from datetime import datetime
from models import Product

# Создаём тур (например, Таиланд, ID=6, цена 120000)
# По нашей БД, на него НЕ было заказов в сентябре 2026, значит должна быть скидка 25%
p = Product(
    product_id=6,
    country="Таиланд",
    city="Пхукет",
    duration=14,
    price=120000.0,
    quantity=5,
    photo="thailand.png"
)

date = datetime(2026, 10, 15) # Дата расчёта

print(f"Базовая цена: {p.price} руб.")
print(f"Цена со скидкой (авто): {p.price_with_discount_auto(date)} руб.")
print(f"Ожидаемая цена (120000 * 0.75): 90000.0 руб.")
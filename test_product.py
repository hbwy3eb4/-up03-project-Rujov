"""Проверка класса Product."""
from models import Product

# Создаём один тур вручную (пример данных)
p = Product(
    product_id=1,
    country="Турция",
    city="Анталья",
    duration=7,
    price=45000,
    quantity=3,
    photo="turkey.jpg"
)

# Выводим информацию
print(p.info())
print(f"Со скидкой 10%: {p.price_with_discount(10):.2f} руб.")
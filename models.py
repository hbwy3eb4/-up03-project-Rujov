"""Модели данных для проекта УП.02 (Туризм)."""
from datetime import datetime
from discount import calculate_price_with_discount

class Product:
    """Класс Товар (в нашем случае — Тур)."""
    
    def __init__(self, product_id, country, city, duration, price, quantity, photo):
        """Инициализация объекта."""
        self.id = product_id
        self.country = country
        self.city = city
        self.duration = duration
        self.price = price
        self.quantity = quantity
        self.photo = photo

    def total(self):
        """Общая стоимость (цена × количество)."""
        return self.price * self.quantity

    def price_with_discount(self, discount_percent):
        """Цена со скидкой (ручной ввод процента)."""
        return self.price * (1 - discount_percent / 100)

    def price_with_discount_auto(self, date=None):
        """Цена со скидкой по алгоритму ДЭ (25%, если нет заказов в прошлом месяце)."""
        if date is None:
            date = datetime.now()
        return calculate_price_with_discount(self.id, self.price, date)

    def indicator(self):
        """Индикатор «много/мало» (порог 5)."""
        return "много" if self.quantity > 5 else "мало"

    def info(self):
        """Строка с информацией о туре."""
        return (
            f"Тур: {self.country}, {self.city} ({self.duration} дн.) | "
            f"Цена: {self.price} руб. × {self.quantity} = {self.total()} руб. "
            f"({self.indicator()}) | Фото: {self.photo}"
        )
    def discounted_price(self):
        """Цена со скидкой 25% (упрощённо, только для тренировки веток)."""
        return self.price * 0.75
    def is_available(self):
        """Товар доступен для заказа?"""
        return self.quantity > 0
    def order_info(self):
       """Информация о заказе."""
       return f"Заказ №{self.id} от {self.date}: {self.client}"

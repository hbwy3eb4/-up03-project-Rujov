"""Расширенное тестирование алгоритма скидки."""
from datetime import datetime
from discount import calculate_price_with_discount

def run_tests():
    """Прогон тестов."""
    test_cases = [
        # Тесты для даты 15.10.2026 (проверка сентября)
        (1, 50000.0, datetime(2026, 10, 15), 50000.0, "Турция — есть заказ в сентябре"),
        (2, 60000.0, datetime(2026, 10, 15), 60000.0, "Египет — есть заказ в сентябре"),
        (3, 80000.0, datetime(2026, 10, 15), 80000.0, "Италия — есть заказ в сентябре"),
        (4, 90000.0, datetime(2026, 10, 15), 67500.0, "Франция — нет заказа в сентябре → скидка 25%"),
        (6, 120000.0, datetime(2026, 10, 15), 90000.0, "Таиланд — нет заказа в сентябре → скидка 25%"),
        
        # Тесты для даты 15.11.2026 (проверка октября)
        # В октябре был заказ только на товар 1 (2026-10-19)
        (1, 50000.0, datetime(2026, 11, 15), 50000.0, "Турция — есть заказ в октябре"),
        (2, 60000.0, datetime(2026, 11, 15), 45000.0, "Египет — нет заказа в октябре → скидка 25%"),
        (4, 90000.0, datetime(2026, 11, 15), 67500.0, "Франция — нет заказа в октябре → скидка 25%"),
        
        # Тест для даты 01.09.2026 (проверка августа)
        # В августе заказов не было вообще
        (1, 50000.0, datetime(2026, 9, 1), 37500.0, "Турция — нет заказа в августе → скидка 25%"),
        (5, 75000.0, datetime(2026, 9, 1), 56250.0, "Испания — нет заказа в августе → скидка 25%"),
    ]
    
    print("=" * 70)
    print("РАСШИРЕННОЕ ТЕСТИРОВАНИЕ АЛГОРИТМА СКИДКИ")
    print("=" * 70)
    
    passed = 0
    for product_id, price, date, expected, comment in test_cases:
        result = calculate_price_with_discount(product_id, price, date)
        result = round(result, 2)
        expected = round(expected, 2)
        
        status = " ✅ " if result == expected else " ❌ "
        if result == expected:
            passed += 1
            
        print(f"{status} Товар {product_id} на {date.date()}: "
              f"{price} → {result} (ожидалось {expected}) — {comment}")
              
    print("=" * 70)
    print(f"Пройдено: {passed} / {len(test_cases)}")
    
    if passed == len(test_cases):
        print(" ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
    else:
        print(f"⚠️  Не пройдено: {len(test_cases) - passed} тестов")

if __name__ == "__main__":
    run_tests()
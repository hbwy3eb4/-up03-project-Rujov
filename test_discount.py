"""Тестирование алгоритма скидки."""
from datetime import datetime
from discount import calculate_price_with_discount

def run_tests():
    """Прогон тестов."""
    date = datetime(2026, 10, 15)  # Дата расчёта: 15 октября 2026 (проверяем сентябрь)
    
    # Данные из вашей БД (db_variant_12.db):
    # Товар 1 (Турция): цена 50000 — БЫЛ заказ в сентябре → без скидки
    # Товар 2 (Египет): цена 60000 — БЫЛ заказ в сентябре → без скидки
    # Товар 4 (Франция): цена 90000 — НЕ БЫЛ заказ в сентябре → скидка 25%
    # Товар 6 (Таиланд): цена 120000 — НЕ БЫЛ заказ в сентябре → скидка 25%
    
    test_cases = [
        # (id_товара, базовая_цена, ожидаемая_цена, "пояснение")
        (1, 50000.0, 50000.0, "Турция — есть заказ в сентябре → без скидки"),
        (2, 60000.0, 60000.0, "Египет — есть заказ в сентябре → без скидки"),
        (4, 90000.0, 67500.0, "Франция — нет заказа в сентябре → скидка 25% (90000 × 0.75)"),
        (6, 120000.0, 90000.0, "Таиланд — нет заказа в сентябре → скидка 25% (120000 × 0.75)"),
    ]
    
    print("=" * 70)
    print("ТЕСТИРОВАНИЕ АЛГОРИТМА СКИДКИ (Дата расчёта: 15.10.2026)")
    print("=" * 70)
    
    passed = 0
    for product_id, price, expected, comment in test_cases:
        result = calculate_price_with_discount(product_id, price, date)
        result = round(result, 2)
        expected = round(expected, 2)
        
        status = " ✅ " if result == expected else " ❌ "
        if result == expected:
            passed += 1
            
        print(f"{status} Товар {product_id}: {price} → {result} "
              f"(ожидалось {expected}) — {comment}")
              
    print("=" * 70)
    print(f"Пройдено: {passed} / {len(test_cases)}")

if __name__ == "__main__":
    run_tests()
"""Модуль отрисовки каталога (карточки товаров)."""
import tkinter as tk
from styles import COLOR_MAIN_BG, COLOR_HIGHLIGHT, get_font
from resources import get_product_image

def create_product_card(parent, product):
    """
    Создаёт карточку товара по макету КИМ.
    product: кортеж (id, страна, город, длительность, цена, количество, фото)
    """
    # Распаковываем данные по индексам вашей БД
    p_id, country, city, duration, price, qty, photo_path = product
    
    # Подсветка: если количество <= 3, фон светло-красный
    bg_color = COLOR_HIGHLIGHT if qty <= 3 else COLOR_MAIN_BG
    
    # Рамка карточки
    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)
    
    # === 1. Изображение (слева) ===
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)
    
    photo = get_product_image(photo_path, size=(100, 100))
    if photo:
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.image = photo  # ВАЖНО: сохраняем ссылку, иначе картинка исчезнет!
        img_label.pack()
    else:
        tk.Label(img_frame, text="[НЕТ ФОТО]", bg=bg_color, width=10, height=5).pack()
    
    # === 2. Текстовая часть (справа) ===
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    
    # Производство | Наименование (для туризма: Страна | Город)
    title = f"{country.upper()} | {city}"
    tk.Label(text_frame, text=title, font=get_font(14, bold=True), 
             bg=bg_color, anchor="w").pack(fill="x")
    
    # Категория (используем страну как категорию)
    tk.Label(text_frame, text=f"Категория: {country}", font=get_font(11), 
             bg=bg_color, anchor="w").pack(fill="x")
    
    # Количество (с индикатором много/мало)
    indicator = "много" if qty > 5 else "мало"
    qty_text = f"Количество: {indicator} ({qty} мест)"
    tk.Label(text_frame, text=qty_text, font=get_font(11), 
             bg=bg_color, anchor="w").pack(fill="x")
    
    # Состав (для туризма: длительность)
    tk.Label(text_frame, text=f"Длительность: {duration} дн.", font=get_font(11), 
             bg=bg_color, anchor="w").pack(fill="x")
    
    # Цена (справа, крупно)
    price_label = tk.Label(text_frame, text=f"{price} руб.", font=get_font(14, bold=True), 
                           bg=bg_color, anchor="e")
    price_label.pack(fill="x")
    
    return card
"""Модуль отрисовки каталога (карточки товаров)."""
import tkinter as tk
from styles import COLOR_MAIN_BG, COLOR_HIGHLIGHT, get_font
from resources import get_product_image
from view_form import ViewForm


def create_product_card(parent, product):
    """Создаёт карточку товара по макету КИМ."""
    # Распаковываем данные по индексам вашей БД
    p_id, country, city, duration, price, qty, photo_path = product
    
    # Подсветка: если количество <= 3, фон светло-красный
    bg_color = COLOR_HIGHLIGHT if qty <= 3 else COLOR_MAIN_BG
    
    # Рамка карточки
    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)
    
    # === ДЕЛАЕМ КАРТОЧКУ КЛИКАБЕЛЬНОЙ ===
    def on_card_click(event):
        """Открывает форму просмотра при клике."""
        ViewForm(parent, product)
        
    # Привязываем клик к самому фрейму карточки
    card.bind("<Button-1>", on_card_click)

    # === 1. Изображение (слева) ===
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)
    img_frame.bind("<Button-1>", on_card_click)
    
    photo = get_product_image(photo_path, size=(100, 100))
    if photo:
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.image = photo  # ВАЖНО: сохраняем ссылку!
        img_label.pack()
        img_label.bind("<Button-1>", on_card_click)
    else:
        lbl = tk.Label(img_frame, text="[НЕТ ФОТО]", bg=bg_color, width=10, height=5)
        lbl.pack()
        lbl.bind("<Button-1>", on_card_click)
    
    # === 2. Текстовая часть (справа) ===
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    text_frame.bind("<Button-1>", on_card_click)
    
    # Производство | Наименование (для туризма: Страна | Город)
    title = f"{country.upper()} | {city}"
    lbl_title = tk.Label(text_frame, text=title, font=get_font(14, bold=True), 
                         bg=bg_color, anchor="w")
    lbl_title.pack(fill="x")
    lbl_title.bind("<Button-1>", on_card_click)
    
    # Категория
    lbl_cat = tk.Label(text_frame, text=f"Категория: {country}", font=get_font(11), 
                       bg=bg_color, anchor="w")
    lbl_cat.pack(fill="x")
    lbl_cat.bind("<Button-1>", on_card_click)
    
    # Количество
    indicator = "много" if qty > 5 else "мало"
    lbl_qty = tk.Label(text_frame, text=f"Количество: {indicator} ({qty} мест)", 
                       font=get_font(11), bg=bg_color, anchor="w")
    lbl_qty.pack(fill="x")
    lbl_qty.bind("<Button-1>", on_card_click)
    
    # Состав (для туризма: длительность)
    lbl_dur = tk.Label(text_frame, text=f"Длительность: {duration} дн.", 
                       font=get_font(11), bg=bg_color, anchor="w")
    lbl_dur.pack(fill="x")
    lbl_dur.bind("<Button-1>", on_card_click)
    
    # Цена (справа, крупно)
    lbl_price = tk.Label(text_frame, text=f"{price} руб.", font=get_font(14, bold=True), 
                         bg=bg_color, anchor="e")
    lbl_price.pack(fill="x")
    lbl_price.bind("<Button-1>", on_card_click)
    
    return card
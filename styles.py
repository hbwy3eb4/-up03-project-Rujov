"""Стили приложения по руководству КИМ."""
import tkinter as tk

# Цвета из КИМ
COLOR_MAIN_BG = "#FFFFFF"       # Основной фон
COLOR_SECONDARY_BG = "#D2F6E7"  # Дополнительный фон (шапка)
COLOR_ACCENT = "#70B2AF"        # Акцент (кнопки)
COLOR_HIGHLIGHT = "#ff8080"     # Подсветка товаров ≤ 3

# Шрифт
FONT_FAMILY = "Calibri"

def get_font(size=12, bold=False):
    """Возвращает кортеж шрифта."""
    weight = "bold" if bold else "normal"
    return (FONT_FAMILY, size, weight)
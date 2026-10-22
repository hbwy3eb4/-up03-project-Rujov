"""Модуль работы с ресурсами (изображения)."""
import os
from PIL import Image, ImageTk

PATH_PICTURE = "resources/picture.png"
PATH_LOGO = "resources/logo.png"
PATH_ICON = "resources/icon.ico"

def load_image(path, size=(100, 100)):
    """Загружает изображение, возвращает PhotoImage или None."""
    try:
        if not os.path.exists(path):
            return None
        img = Image.open(path).resize(size)
        return ImageTk.PhotoImage(img)
    except Exception:
        return None

def get_product_image(image_path, size=(100, 100)):
    """Возвращает фото товара или заглушку picture.png."""
    # Если путь пустой или файла нет, берём заглушку
    if not image_path or not os.path.exists(image_path):
        return load_image(PATH_PICTURE, size)
    return load_image(image_path, size)
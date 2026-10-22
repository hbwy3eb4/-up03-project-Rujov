"""Главное окно приложения с каталогом и авторизацией."""
import tkinter as tk
from tkinter import ttk
import os

from styles import COLOR_SECONDARY_BG, COLOR_ACCENT, get_font
from database import get_all_products
from catalog import create_product_card
from resources import load_image, PATH_LOGO, PATH_ICON


class CatalogApp:
    """Главное приложение каталога туров с авторизацией."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Система заказа туров")
        self.root.geometry("800x600")
        
        self.current_user = None  # Данные авторизованного пользователя
        self.user_label = None    # Метка для отображения ФИО
        self.orders_btn = None    # Кнопка "Заказы"
        
        self.set_icon()
        self.build_ui()
        self.load_products()
        
        # Запрашиваем авторизацию при запуске
        self.require_auth()

    def require_auth(self):
        """Запрашивает авторизацию при старте."""
        from auth import AuthWindow
        AuthWindow(self.root, self.on_auth_success)

    def on_auth_success(self, user):
        """
        Обработчик успешной авторизации.
        :param user: кортеж (id, фамилия, имя, отчество, логин, роль)
        """
        self.current_user = user
        # Отображаем ФИО и роль в шапке
        fio = f"{user[1]} {user[2]} {user[3] or ''}".strip()
        if self.user_label:
            self.user_label.config(text=f"{fio} ({user[5]})")
        
        # Добавляем кнопки в зависимости от роли
        self.add_role_buttons(user[5])

    def add_role_buttons(self, role):
        """Добавляет кнопки в шапку в зависимости от роли."""
        if role in ("Менеджер", "Администратор"):
            self.orders_btn = tk.Button(
                self.user_label.master, text="Заказы", command=self.open_orders,
                bg=COLOR_ACCENT, fg="white", font=get_font(12),
                padx=10, pady=5
            )
            self.orders_btn.pack(side="right", padx=10)

    def open_orders(self):
        """Открывает окно списка заказов."""
        try:
            from orders_window import OrdersWindow
            OrdersWindow(self.root, self.current_user)
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Ошибка", f"Не удалось открыть список заказов:\n{e}")

    def set_icon(self):
        try:
            if os.name == "nt":
                if os.path.exists(PATH_ICON):
                    self.root.iconbitmap(PATH_ICON)
            else:
                img = load_image(PATH_ICON.replace(".ico", ".png"), size=(32, 32))
                if img:
                    self.root.iconphoto(True, img)
                    self.root._icon_photo = img
        except Exception:
            pass

    def build_ui(self):
        """Строит интерфейс главного окна."""
        header = tk.Frame(self.root, bg=COLOR_SECONDARY_BG, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Логотип слева
        logo = load_image(PATH_LOGO, size=(60, 60))
        if logo:
            logo_label = tk.Label(header, image=logo, bg=COLOR_SECONDARY_BG)
            logo_label.image = logo
            logo_label.pack(side="left", padx=15, pady=10)
        else:
            tk.Label(header, text="[ЛОГОТИП]", bg=COLOR_SECONDARY_BG).pack(side="left", padx=15)

        # Заголовок по центру
        tk.Label(header, text="КАТАЛОГ ТУРОВ", font=get_font(18, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(expand=True)

        # ФИО пользователя (правый верхний угол)
        self.user_label = tk.Label(header, text="Не авторизован",
                                   font=get_font(12),
                                   bg=COLOR_SECONDARY_BG)
        self.user_label.pack(side="right", padx=15)

        # Область с прокруткой для карточек
        self.canvas = tk.Canvas(self.root, bg="#FFFFFF", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)

        self.catalog_frame = tk.Frame(self.canvas, bg="#FFFFFF")
        self.catalog_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.catalog_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_products(self):
        """Загружает туры из БД и создаёт карточки."""
        products = get_all_products()
        for p in products:
            create_product_card(self.catalog_frame, p)

    def run(self):
        """Запускает приложение."""
        self.root.mainloop()


if __name__ == "__main__":
    app = CatalogApp()
    app.run()
"""Авторизация пользователей."""
import tkinter as tk
from tkinter import messagebox
from styles import COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT, get_font
from database import get_user_by_login


class AuthWindow:
    """Окно авторизации."""
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.window = tk.Toplevel(root)
        self.window.title("Авторизация")
        self.window.geometry("400x300")
        self.window.configure(bg=COLOR_MAIN_BG)
        self.window.grab_set()  # Делает окно модальным (блокирует главное)
        self.build_ui()

    def build_ui(self):
        """Строит интерфейс окна."""
        # Шапка
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="ВХОД В СИСТЕМУ", font=get_font(16, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        # Поле ввода логина
        form = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        form.pack(pady=30)
        tk.Label(form, text="Логин:", font=get_font(12),
                 bg=COLOR_MAIN_BG).pack(anchor="w")
        
        self.login_var = tk.StringVar()
        tk.Entry(form, textvariable=self.login_var, width=30,
                 font=get_font(12)).pack(pady=5)

        # Кнопка входа
        tk.Button(form, text="Войти", command=self.login,
                  bg=COLOR_ACCENT, fg="white",
                  font=get_font(12),
                  padx=20, pady=5).pack(pady=15)

        # Подсказка
        tk.Label(form, text="Пример: manager1, admin1, client1",
                 font=get_font(11), fg="gray", bg=COLOR_MAIN_BG).pack()

    def login(self):
        """Обработчик входа."""
        login = self.login_var.get().strip()
        if not login:
            messagebox.showwarning("Ошибка", "Введите логин")
            return
            
        user = get_user_by_login(login)
        if not user:
            messagebox.showerror("Ошибка", "Пользователь не найден")
            return
            
        messagebox.showinfo("Успех", f"Добро пожаловать, {user[1]} {user[2]}!")
        self.window.destroy()
        self.on_success(user)  # Передаём данные пользователя в главное окно
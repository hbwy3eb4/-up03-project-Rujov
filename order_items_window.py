"""Окно состава заказа с функциями редактирования для Администратора."""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from styles import COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT, get_font
import order_manager as om


class OrderItemsWindow:
    """Окно состава заказа."""
    def __init__(self, parent, order_id, current_user=None):
        self.order_id = order_id
        self.current_user = current_user
        self.window = tk.Toplevel(parent)
        self.window.title(f"Состав заказа №{order_id}")
        self.window.geometry("850x550")
        self.window.configure(bg=COLOR_MAIN_BG)
        self.build_ui()
        self.load_order_info()
        self.load_items()

    def is_admin(self):
        """Проверяет, является ли пользователь Администратором."""
        return self.current_user and self.current_user[5] == "Администратор"

    def build_ui(self):
        # Шапка
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text=f"СОСТАВ ЗАКАЗА №{self.order_id}",
                 font=get_font(16, bold=True), bg=COLOR_SECONDARY_BG).pack(pady=15)

        # Информация о заказе (Дата и Клиент)
        info_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        info_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(info_frame, text="Дата заказа:", font=get_font(12, bold=True),
                 bg=COLOR_MAIN_BG).pack(side="left", padx=5)

        self.date_var = tk.StringVar()
        self.date_entry = tk.Entry(info_frame, textvariable=self.date_var,
                                   width=12, font=get_font(12), state="readonly")
        self.date_entry.pack(side="left", padx=5)

        # Кнопка сохранения даты ТОЛЬКО для Администратора
        if self.is_admin():
            self.date_entry.config(state="normal")
            tk.Button(info_frame, text="Сохранить дату", command=self.save_date,
                      bg=COLOR_ACCENT, fg="white", font=get_font(11),
                      padx=10, pady=3).pack(side="left", padx=10)

        tk.Label(info_frame, text="Клиент:", font=get_font(12, bold=True),
                 bg=COLOR_MAIN_BG).pack(side="left", padx=20)
        self.client_label = tk.Label(info_frame, text="", font=get_font(12), bg=COLOR_MAIN_BG)
        self.client_label.pack(side="left")

        # Таблица позиций (адаптировано под Туризм: Страна, Город, Кол-во, Цена)
        columns = ("id", "country", "city", "quantity", "price", "total")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings", height=12)
        self.tree.heading("id", text="№")
        self.tree.heading("country", text="Страна")
        self.tree.heading("city", text="Город")
        self.tree.heading("quantity", text="Кол-во чел.")
        self.tree.heading("price", text="Цена за тур")
        self.tree.heading("total", text="Сумма")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("country", width=150, anchor="w")
        self.tree.column("city", width=150, anchor="w")
        self.tree.column("quantity", width=100, anchor="center")
        self.tree.column("price", width=120, anchor="e")
        self.tree.column("total", width=120, anchor="e")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        # Итоговая сумма
        self.total_label = tk.Label(self.window, text="", font=get_font(14, bold=True),
                                    fg=COLOR_ACCENT, bg=COLOR_MAIN_BG)
        self.total_label.pack(pady=5)

        # Кнопки управления
        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", pady=10)

        # Кнопка удаления позиции ТОЛЬКО для Администратора
        if self.is_admin():
            tk.Button(btn_frame, text="Удалить позицию", command=self.delete_item,
                      bg="#ff8080", fg="white", font=get_font(12),
                      padx=15, pady=5).pack(side="left", padx=20)

        tk.Button(btn_frame, text="Обновить", command=self.refresh_all,
                  bg=COLOR_ACCENT, fg="white", font=get_font(12),
                  padx=15, pady=5).pack(side="left", padx=10)

        tk.Button(btn_frame, text="Назад", command=self.window.destroy,
                  bg=COLOR_ACCENT, fg="white", font=get_font(12),
                  padx=15, pady=5).pack(side="right", padx=20)

    def load_order_info(self):
        """Загружает информацию о заказе (дата, клиент)."""
        order = om.get_order_by_id(self.order_id)
        if order:
            self.date_var.set(order[1])  # order[1] = дата
            self.client_label.config(text=order[2])  # order[2] = клиент

    def load_items(self):
        """Загружает позиции заказа из БД."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            items = om.get_order_items(self.order_id)
            if not items:
                self.total_label.config(text="ИТОГО: 0.00 руб.")
                return

            total = 0.0
            for item in items:
                # item = (id, страна, город, количество, цена)
                item_id = item[0]
                country = item[1]
                city = item[2]
                quantity = item[3]
                price = item[4]
                item_total = quantity * price
                total += item_total

                self.tree.insert("", tk.END, values=(item_id, country, city, quantity,
                                                     f"{price:.2f}", f"{item_total:.2f}"))

            self.total_label.config(text=f"ИТОГО ПО ЗАКАЗУ: {total:.2f} руб.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить состав:\n{e}")

    def save_date(self):
        """Сохраняет изменённую дату заказа."""
        new_date = self.date_var.get().strip()
        # Валидация формата даты YYYY-MM-DD
        try:
            datetime.strptime(new_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД")
            return

        if om.update_order_date(self.order_id, new_date):
            messagebox.showinfo("Успех", "Дата заказа успешно обновлена!")
            self.refresh_all()
        else:
            messagebox.showerror("Ошибка", "Не удалось обновить дату в базе данных.")

    def delete_item(self):
        """Удаляет выбранную позицию и восстанавливает остатки."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите позицию для удаления")
            return

        item = self.tree.item(selected[0])
        item_id = item["values"][0]
        country = item["values"][1]

        if not messagebox.askyesno("Подтверждение",
                                   f"Удалить позицию '{country}' из заказа?\n"
                                   f"Количество мест будет возвращено на склад."):
            return

        if om.delete_order_item(item_id):
            messagebox.showinfo("Успех", "Позиция удалена, остатки восстановлены!")
            self.refresh_all()
        else:
            messagebox.showerror("Ошибка", "Не удалось удалить позицию.")

    def refresh_all(self):
        """Обновляет всю информацию в окне."""
        self.load_order_info()
        self.load_items()
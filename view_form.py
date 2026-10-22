"""Форма просмотра товара (тура)."""
import tkinter as tk
from tkinter import messagebox
from styles import COLOR_MAIN_BG, COLOR_ACCENT, COLOR_SECONDARY_BG, get_font
from resources import get_product_image
from order_manager import add_order_to_db, update_product_quantity, get_product_quantity


class ViewForm:
    def __init__(self, parent, product, on_order_success=None):
        """
        :param parent: родительское окно
        :param product: кортеж с данными тура из БД
        :param on_order_success: callback для обновления каталога после заказа
        """
        self.product = product
        self.on_order_success = on_order_success  # callback для обновления каталога
        self.window = tk.Toplevel(parent)
        self.window.title(f"Тур: {product[1]} - {product[2]}")
        self.window.geometry("600x500")
        self.window.configure(bg=COLOR_MAIN_BG)
        
        # Делаем окно модальным (поверх главного)
        self.window.transient(parent)
        self.window.grab_set()
        
        self.build_ui()

    def build_ui(self):
        # === Шапка ===
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="КАРТОЧКА ТУРА", font=get_font(16, bold=True), 
                 bg=COLOR_SECONDARY_BG).pack(pady=15)
        
        # === Основная область ===
        main = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        # --- Изображение (слева) ---
        img_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        img_frame.pack(side="left", padx=10)
        
        # product[6] — это поле 'фото' в вашей БД
        photo = get_product_image(self.product[6], size=(200, 200))
        if photo:
            img_label = tk.Label(img_frame, image=photo, bg=COLOR_MAIN_BG)
            img_label.image = photo  # Сохраняем ссылку!
            img_label.pack()
        else:
            tk.Label(img_frame, text="[НЕТ ФОТО]", bg=COLOR_MAIN_BG, width=15, height=10).pack()
            
        # --- Информация (справа) ---
        info_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        info_frame.pack(side="left", fill="both", expand=True, padx=20)
        
        # Адаптация под Туризм:
        # product[1]=страна, [2]=город, [3]=длительность, [4]=цена, [5]=количество
        self._add_field(info_frame, "Страна", self.product[1])
        self._add_field(info_frame, "Город", self.product[2])
        self._add_field(info_frame, "Длительность", f"{self.product[3]} дн.")
        self._add_field(info_frame, "Количество мест", self.product[5])
        self._add_field(info_frame, "Цена", f"{self.product[4]} руб.")
        
        # === Поля ввода для заказа ===
        form_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        form_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(form_frame, text="ФИО клиента:", font=get_font(11, bold=True), 
                 bg=COLOR_MAIN_BG).pack(anchor="w")
        self.entry_fio = tk.Entry(form_frame, font=get_font(11), width=40)
        self.entry_fio.pack(fill="x", pady=(0, 10))
        
        tk.Label(form_frame, text="Количество человек:", font=get_font(11, bold=True), 
                 bg=COLOR_MAIN_BG).pack(anchor="w")
        self.entry_qty = tk.Entry(form_frame, font=get_font(11), width=10)
        self.entry_qty.insert(0, "1")  # По умолчанию 1
        self.entry_qty.pack(fill="x", pady=(0, 10))
        
        # === Кнопки (внизу) ===
        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", pady=10)
        
        # ВАЖНО: кнопка теперь вызывает submit_order (реальная логика БД)
        tk.Button(btn_frame, text="Оформить заказ", font=get_font(12, bold=True), 
                  bg=COLOR_ACCENT, fg="white", command=self.submit_order).pack(side="left", padx=20, expand=True, fill="x")
                  
        tk.Button(btn_frame, text="Назад", font=get_font(12), 
                  bg="#cccccc", command=self.window.destroy).pack(side="right", padx=20, expand=True, fill="x")

    def _add_field(self, parent, label, value):
        """Добавляет строку с полем."""
        row = tk.Frame(parent, bg=COLOR_MAIN_BG)
        row.pack(fill="x", pady=5)
        tk.Label(row, text=f"{label}:", font=get_font(12, bold=True), 
                 bg=COLOR_MAIN_BG, width=15, anchor="w").pack(side="left")
        tk.Label(row, text=str(value), font=get_font(12), 
                 bg=COLOR_MAIN_BG, anchor="w").pack(side="left", fill="x", expand=True)

    def submit_order(self):
        """Обработчик кнопки «Оформить заказ» — сохраняет заказ в БД."""
        fio = self.entry_fio.get().strip()
        qty_str = self.entry_qty.get().strip()
        
        # 1. Проверка заполненности полей
        if not fio or not qty_str:
            messagebox.showwarning("Ошибка", "Заполните ФИО и количество!")
            return
            
        try:
            qty_to_order = int(qty_str)
            if qty_to_order <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Количество должно быть целым числом > 0")
            return

        # 2. Логика сохранения в БД
        try:
            # Получаем текущее количество мест из БД
            current_qty = get_product_quantity(self.product[0])  # product[0] = id товара
            
            # Проверяем, хватает ли мест
            if current_qty < qty_to_order:
                messagebox.showwarning("Ошибка", 
                    f"Недостаточно мест! Доступно только {current_qty}.")
                return
            
            # Сохраняем заказ в таблицу "Заказ"
            add_order_to_db(fio, self.product[0], qty_to_order)
            
            # Уменьшаем количество мест в таблице "Товар"
            new_qty = current_qty - qty_to_order
            update_product_quantity(self.product[0], new_qty)
            
            messagebox.showinfo("Успех", 
                f"Заказ для {fio} на {qty_to_order} чел. успешно создан!")
            
            # Закрываем окно
            self.window.destroy()
            
            # Вызываем callback для обновления каталога (если передан)
            if self.on_order_success:
                self.on_order_success()
            
        except Exception as e:
            messagebox.showerror("Ошибка БД", f"Не удалось оформить заказ:\n{e}")
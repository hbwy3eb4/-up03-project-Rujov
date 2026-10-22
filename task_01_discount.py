import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


class DB:
    def __init__(self, db="db.db"):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()

    # --- ЧТЕНИЕ ---
    def get_all(self, table):
        self.cur.execute(f"SELECT * FROM {table}")
        return self.cur.fetchall()

    def get_by_id(self, table, id_):
        self.cur.execute(f"SELECT * FROM {table} WHERE id = ?", (id_,))
        return self.cur.fetchone()

    # --- ДОБАВЛЕНИЕ ---
    def insert(self, table, values):
        placeholders = ",".join(["?"] * len(values))
        self.cur.execute(f"INSERT INTO {table} VALUES (NULL,{placeholders})", values)
        self.con.commit()

    # --- ОБНОВЛЕНИЕ ---
    def update(self, table, id_, values):
        set_clause = ",".join([f"col{i+1}=?" for i in range(len(values))])
        self.cur.execute(f"UPDATE {table} SET {set_clause} WHERE id=?", (*values, id_))
        self.con.commit()

    # --- УДАЛЕНИЕ ---
    def delete(self, table, id_):
        self.cur.execute(f"DELETE FROM {table} WHERE id=?", (id_,))
        self.con.commit()


class App:
    def __init__(self, root):
        self.root = root
        self.db = DB("db_variant_12.db")
        self.TABLE = "Товар"          # ← меняешь под свой проект
        self.COLS = ("id","страна","город","длительность","цена","количество")  # ← свои колонки
        self.HEADERS = ("ID","Страна","Город","Дней","Цена","Мест")

        root.title("Приложение")
        root.geometry("700x500")

        self.show_list()

    # ========== СПИСОК ==========
    def show_list(self):
        self._clear()
        tk.Label(self.root, text="Список", font=("Arial",14)).pack(pady=5)

        self.tree = ttk.Treeview(self.root, columns=self.COLS, show="headings", height=15)
        for h, c in zip(self.HEADERS, self.COLS):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=100)
        self.tree.pack(fill="both", expand=True, padx=10)

        self._refresh()

        frm = tk.Frame(self.root)
        frm.pack(pady=5)
        tk.Button(frm, text="Добавить", command=self.show_form).pack(side="left", padx=5)
        tk.Button(frm, text="Изменить", command=self.show_form_edit).pack(side="left", padx=5)
        tk.Button(frm, text="Удалить", command=self._delete).pack(side="left", padx=5)
        tk.Button(frm, text="Выход", command=self.root.quit).pack(side="right", padx=5)

    def _refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in self.db.get_all(self.TABLE):
            self.tree.insert("", "end", values=row)

    def _clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    # ========== ФОРМА (добавление/редактирование) ==========
    def show_form(self, row=None):
        self._clear()
        tk.Label(self.root, text="Форма", font=("Arial",14)).pack(pady=10)

        entries = []
        for i, col in enumerate(self.COLS[1:], 1):  # пропускаем id
            tk.Label(self.root, text=col).pack()
            e = tk.Entry(self.root)
            e.pack()
            if row:
                e.insert(0, row[i])
            entries.append(e)

        def save():
            vals = [e.get() for e in entries]
            if row:
                self.db.update(self.TABLE, row[0], vals)
            else:
                self.db.insert(self.TABLE, vals)
            self.show_list()

        tk.Button(self.root, text="Сохранить", command=save).pack(pady=10)
        tk.Button(self.root, text="Отмена", command=self.show_list).pack()

    def show_form_edit(self):
        sel = self.tree.selection()
        if not sel:
            return messagebox.showwarning("","Выберите строку")
        row = self.tree.item(sel[0])["values"]
        self.show_form(row)

    # ========== УДАЛЕНИЕ ==========
    def _delete(self):
        sel = self.tree.selection()
        if not sel:
            return messagebox.showwarning("","Выберите строку")
        if messagebox.askyesno("","Удалить?"):
            id_ = self.tree.item(sel[0])["values"][0]
            self.db.delete(self.TABLE, id_)
            self._refresh()


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
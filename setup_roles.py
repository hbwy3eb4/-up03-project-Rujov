"""Создание таблиц Роль и Пользователь для авторизации."""
import sqlite3
from config import DB_PATH

def setup_roles_and_users():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # 1. Создаём таблицу Роль
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Роль (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            название TEXT NOT NULL UNIQUE
        )
    """)
    
    # 2. Создаём таблицу Пользователь (нормализованная структура)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Пользователь (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            фамилия TEXT NOT NULL,
            имя TEXT NOT NULL,
            отчество TEXT,
            логин TEXT NOT NULL UNIQUE,
            роль_id INTEGER NOT NULL,
            FOREIGN KEY (роль_id) REFERENCES Роль(id)
        )
    """)
    
    # 3. Заполняем роли
    roles = [('Клиент',), ('Менеджер',), ('Администратор',)]
    for role in roles:
        try:
            cur.execute("INSERT INTO Роль (название) VALUES (?)", role)
        except sqlite3.IntegrityError:
            pass  # Роль уже существует
    
    # 4. Заполняем пользователей
    users = [
        ('Иванов', 'Иван', 'Иванович', 'client1', 1),
        ('Петров', 'Петр', 'Петрович', 'manager1', 2),
        ('Сидоров', 'Сидор', 'Сидорович', 'admin1', 3),
    ]
    for user in users:
        try:
            cur.execute(
                "INSERT INTO Пользователь (фамилия, имя, отчество, логин, роль_id) VALUES (?, ?, ?, ?, ?)",
                user
            )
        except sqlite3.IntegrityError:
            pass  # Пользователь уже существует
    
    conn.commit()
    conn.close()
    print("✅ Таблицы Роль и Пользователь созданы и заполнены!")

if __name__ == "__main__":
    setup_roles_and_users()
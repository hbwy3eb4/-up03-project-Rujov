"""Удаление старых таблиц и создание новых."""
import sqlite3
from config import DB_PATH

def reset_tables():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Удаляем старые таблицы (если они есть)
    cur.execute("DROP TABLE IF EXISTS Пользователь")
    cur.execute("DROP TABLE IF EXISTS Роль")
    
    # Создаём таблицу Роль
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Роль (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            название TEXT NOT NULL UNIQUE
        )
    """)
    
    # Создаём таблицу Пользователь (нормализованная структура)
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
    
    # Заполняем роли
    roles = [('Клиент',), ('Менеджер',), ('Администратор',)]
    for role in roles:
        cur.execute("INSERT INTO Роль (название) VALUES (?)", role)
    
    # Заполняем пользователей
    users = [
        ('Иванов', 'Иван', 'Иванович', 'client1', 1),
        ('Петров', 'Петр', 'Петрович', 'manager1', 2),
        ('Сидоров', 'Сидор', 'Сидорович', 'admin1', 3),
    ]
    for user in users:
        cur.execute(
            "INSERT INTO Пользователь (фамилия, имя, отчество, логин, роль_id) VALUES (?, ?, ?, ?, ?)",
            user
        )
    
    conn.commit()
    conn.close()
    print("✅ Таблицы Роль и Пользователь созданы заново!")

if __name__ == "__main__":
    reset_tables()
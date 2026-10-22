-- Создаём таблицу Состав_заказа
CREATE TABLE IF NOT EXISTS Состав_заказа (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    заказ_id INTEGER NOT NULL,
    товар_id INTEGER NOT NULL,
    количество INTEGER NOT NULL,
    цена REAL NOT NULL,
    FOREIGN KEY (заказ_id) REFERENCES Заказ(id) ON DELETE CASCADE,
    FOREIGN KEY (товар_id) REFERENCES Товар(id)
);
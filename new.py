import sqlite3
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
app = Flask(__name__)

conn = sqlite3.connect('restaurant.db')

# создаем курсор для работы с базой данных
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                address TEXT,
                time TEXT,
                dishList TEXT,
                is_deleted INTEGER DEFAULT 0,
                status TEXT,
                phone TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )''')

cur.execute("INSERT INTO orders (id, user_id, address, time, dishList, is_deleted, status, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (1, 1, "Some address", "Some time", json.dumps([
                {
                    "id": 1,
                    "value": 2
                },
                {
                    "id": 2,
                    "value": 3
                },
                {
                    "id": 3,
                    "value": 1
                }
            ]), 0, "pending", "1234567890"))
# cur.execute("DROP TABLE IF EXISTS orders")
# Сохраняем изменения в базе данных
conn.commit()

# Закрываем соединение с базой данных
conn.close()
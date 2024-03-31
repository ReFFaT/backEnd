import sqlite3
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
app = Flask(__name__)

conn = sqlite3.connect('restaurant.db')

# создаем курсор для работы с базой данных
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    dish_list TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_deleted INTEGER DEFAULT 0
)''')
# Сохраняем изменения в базе данных
conn.commit()

# Закрываем соединение с базой данных
conn.close()
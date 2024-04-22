
import sqlite3
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
CORS(app)
# получение меню
@app.route('/menu', methods=['GET'])
def get_menu():
    conn = sqlite3.connect('restaurant.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM menu")
    menu_table = cur.fetchall()

    menu_data = []
    for row in menu_table:
        menu_item = {
            'id': row[0],
            'title': row[1],
            'dishList': json.loads(row[2])
        }
        menu_data.append(menu_item)

    conn.close()

    return jsonify(menu_data)

# добавление меню
@app.route('/menu', methods=['POST'])
def add_menu_item():
    try:
        # Получение данных из запроса
        menu_data = request.json
        title = menu_data['title']

        # Открытие соединения с базой данных
        conn = sqlite3.connect('restaurant.db')
        cur = conn.cursor()

        # Добавление записи в таблицу меню
        cur.execute("INSERT INTO menu (title) VALUES (?)", (title,))

        # Получение данных из таблицы всех блюд, соответствующих новому разделу
        cur.execute("SELECT * FROM all_dishes WHERE type = ? AND selected = 'true'", (title,))
        dish_rows = cur.fetchall()

        # Обновление dishList для нового раздела в таблице меню
        dishList = []
        for row in dish_rows:
            dish_item = {
                'id': row[0],
                'image': row[1],
                'name': row[2],
                'title': row[3],
                'price': row[4],
                'gram': row[5],
                'type': row[6]
            }
            dishList.append(dish_item)

        cur.execute("UPDATE menu SET dishList = ? WHERE title = ?", (json.dumps(dishList), title))

        conn.commit()
        conn.close()

        return jsonify({'message': 'Menu item added successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

# обновление меню
@app.route('/menu/<int:menu_id>', methods=['PUT'])
def update_menu(menu_id):
    try:
        # Получение данных из запроса
        menu_data = request.json
        title = menu_data['title']

        # Открытие соединения с базой данных
        conn = sqlite3.connect('restaurant.db')
        cur = conn.cursor()

        # Получение блюд из таблицы all_dishes, соответствующих указанному заголовку и флагу активности
        cur.execute("SELECT * FROM all_dishes WHERE type = ? AND selected = 'true'", (title,))
        dish_rows = cur.fetchall()

        # Обновление dishList в таблице меню
        dishList = []
        for row in dish_rows:
            dish_item = {
                'id': row[0],
                'image': row[1],
                'name': row[2],
                'title': row[3],
                'price': row[4],
                'gram': row[5],
                'type': row[6]
            }
            dishList.append(dish_item)

        cur.execute("UPDATE menu SET title = ?, dishList = ? WHERE id = ?", (title, json.dumps(dishList), menu_id))

        conn.commit()
        conn.close()

        return jsonify({'message': 'Menu item updated successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# удаление меню
@app.route('/menu/<int:item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    try:
        # Открытие соединения с базой данных
        conn = sqlite3.connect('restaurant.db')
        cur = conn.cursor()

        # Удаление записи из таблицы меню по ID
        cur.execute("DELETE FROM menu WHERE id=?", (item_id,))

        # Сохраняем изменения в базе данных
        conn.commit()

        # Закрываем соединение с базой данных
        conn.close()

        return jsonify({'message': 'Menu item deleted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    







                                                                                                                        # блюда

# создание блюда
@app.route('/dishes', methods=['POST'])
def add_dish():
    try:
        # Получение данных из запроса
        dish_data = request.json
        image = dish_data['image']
        name = dish_data['name']
        title = dish_data['title']
        price = dish_data['price']
        gram = dish_data['gram']
        dish_type = dish_data['type']
        selected = dish_data['selected']

        # Открытие соединения с базой данных
        conn = sqlite3.connect('restaurant.db')
        cur = conn.cursor()

        # Добавление записи в таблицу всех блюд
        cur.execute("INSERT INTO all_dishes (image, name, title, price, gram, type, selected) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (image, name, title, price, gram, dish_type, selected))
        cur.execute("UPDATE menu SET dishList = (SELECT json_group_array(json_object('id', all_dishes.id, 'image', all_dishes.image, 'name', all_dishes.name, 'title', all_dishes.title, 'price', all_dishes.price, 'gram', all_dishes.gram, 'type', all_dishes.type)) FROM all_dishes WHERE all_dishes.type = menu.title AND all_dishes.selected = 'true')")

        conn.commit()
        conn.close()

        return jsonify({'message': 'Dish added successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400
# {
#   "image": "steak.svg",
#   "name": "Стейк",
#   "title": "Описание стейка",
#   "price": 400,
#   "gram": 600,
#   "type": "Горячие блюда",
#   "selected": "true"
# }    

# удаление блюда
@app.route('/dishes/<int:dish_id>', methods=['DELETE'])
def delete_dish(dish_id):
    try:
        # Открытие соединения с базой данных
        conn = sqlite3.connect('restaurant.db')
        cur = conn.cursor()

        # Удаление записи из таблицы всех блюд по заданному ID
        cur.execute("DELETE FROM all_dishes WHERE id = ?", (dish_id,))
        cur.execute("UPDATE menu SET dishList = (SELECT json_group_array(json_object('id', all_dishes.id, 'image', all_dishes.image, 'name', all_dishes.name, 'title', all_dishes.title, 'price', all_dishes.price, 'gram', all_dishes.gram, 'type', all_dishes.type)) FROM all_dishes WHERE all_dishes.type = menu.title AND all_dishes.selected = 'true')")

        conn.commit()
        conn.close()

        return jsonify({'message': 'Dish deleted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    


# обновление блюда
@app.route('/dishes/<int:dish_id>', methods=['PUT'])
def update_dish(dish_id):
    try:
        # Получение данных из запроса
        dish_data = request.json
        image = dish_data['image']
        name = dish_data['name']
        title = dish_data['title']
        price = dish_data['price']
        gram = dish_data['gram']
        type = dish_data['type']
        selected = dish_data['selected']

        # Открытие соединения с базой данных
        with sqlite3.connect('restaurant.db') as conn:
            cur = conn.cursor()

            # Обновление записи в таблице всех блюд по ID
            cur.execute("UPDATE all_dishes SET image=?, name=?, title=?, price=?, gram=?, type=?, selected=? WHERE id=?",
                        (image, name, title, price, gram, type, selected, dish_id))

            # Обновление таблицы меню с учетом изменений
            cur.execute("UPDATE menu SET dishList = (SELECT json_group_array(json_object('id', all_dishes.id, 'image', all_dishes.image, 'name', all_dishes.name, 'title', all_dishes.title, 'price', all_dishes.price, 'gram', all_dishes.gram, 'type', all_dishes.type)) FROM all_dishes WHERE all_dishes.type = menu.title AND all_dishes.selected = 'true')")

            conn.commit()

        return jsonify({'message': 'Dish updated successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400
# {
#   "image": "new_image.svg",
#   "name": "Новое блюдо",
#   "title": "Описание нового блюда",
#   "price": 500,
#   "gram": 800,
#   "type": "Горячие блюда",
#   "selected": "true"
# }


# получение блюда
@app.route('/dishes/<int:dish_id>', methods=['GET'])
def get_dish(dish_id):
    try:
        # Открытие соединения с базой данных
        with sqlite3.connect('restaurant.db') as conn:
            cur = conn.cursor()

            # Получение записи из таблицы всех блюд по ID
            cur.execute("SELECT * FROM all_dishes WHERE id=?", (dish_id,))
            dish = cur.fetchone()

            if dish is None:
                return jsonify({'error': 'Dish not found'}), 404

            # Формирование объекта блюда
            dish_data = {
                'id': dish[0],
                'image': dish[1],
                'name': dish[2],
                'title': dish[3],
                'price': dish[4],
                'gram': dish[5],
                'type': dish[6],
                'selected': dish[7]
            }

        return jsonify(dish_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# получение всех блюд
@app.route('/dishes', methods=['GET'])
def get_all_dishes():
    try:
        # Открытие соединения с базой данных
        with sqlite3.connect('restaurant.db') as conn:
            cur = conn.cursor()

            # Получение всех записей из таблицы всех блюд
            cur.execute("SELECT * FROM all_dishes")
            dishes = cur.fetchall()

            # Формирование списка объектов блюд
            dish_list = []
            for dish in dishes:
                dish_data = {
                    'id': dish[0],
                    'image': dish[1],
                    'name': dish[2],
                    'title': dish[3],
                    'price': dish[4],
                    'gram': dish[5],
                    'type': dish[6],
                    'selected': dish[7]
                }
                dish_list.append(dish_data)

        return jsonify(dish_list)

    except Exception as e:
        return jsonify({'error': str(e)}), 400


                                                                                                                        # пользователи
# Получение всех пользователей
@app.route('/users', methods=['GET'])
def get_users():
    try:
        conn = sqlite3.connect('restaurant.db')
        cur = conn.cursor()

        cur.execute("SELECT * FROM users")
        users = cur.fetchall()

        user_list = []
        for user in users:
            user_data = {
                'id': user[0],
                'name': user[1],
                'email': user[2],
                'password': user[3],
                'role': user[4]
            }
            user_list.append(user_data)

        conn.close()

        return jsonify(user_list)

    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Получение конкретного пользователя
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        conn = sqlite3.connect('restaurant.db')
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
        user = cur.fetchone()

        if user is None:
            return jsonify({'error': 'User not found'}), 404

        user_data = {
            'id': user[0],
            'name': user[1],
            'email': user[2],
            'password': user[3],
            'role': user[4],
            'authorized': True
        }

        conn.close()

        return jsonify(user_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Обновление пользователя
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        conn = sqlite3.connect('restaurant.db')
        cur = conn.cursor()

        user_data = request.json

        # Проверка наличия обязательных полей
        if 'name' not in user_data or 'email' not in user_data or 'password' not in user_data or 'role' not in user_data:
            return jsonify({'error': 'Missing required fields'}), 400

        name = user_data['name']
        email = user_data['email']
        password = user_data['password']
        role = user_data['role']

        cur.execute("UPDATE users SET name=?, email=?, password=?, role=? WHERE id=?",
                    (name, email, password, role, user_id))
        conn.commit()
        conn.close()

        return jsonify({'message': 'User updated successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400
# {
#   "name": "Новое имя",
#   "email": "новыйemail@example.com",
#   "password": "новыйпароль",
#   "role": "новаяроль"
# }

# создание
@app.route('/register', methods=['POST'])
def register_user():
    try:
        conn = sqlite3.connect('restaurant.db')
        cur = conn.cursor()
        # Получение данных из запроса
        user_data = request.json
        name = user_data['name']
        email = user_data['email']
        password = user_data['password']
        
        # Установка роли пользователя
        role = 'user'
        
        # Вставка данных в таблицу пользователей
        cur.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                    (name, email, password, role))
        conn.commit()
        
        # Закрытие соединения с базой данных
        conn.close()
        
        return jsonify({'message': 'User registered successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
# {
#   "name": "John Doe",
#   "email": "johndoe@example.com",
#   "password": "password123"
# }

# Удаление пользователя
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = sqlite3.connect('restaurant.db')
        cur = conn.cursor()

        cur.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()
        conn.close()

        return jsonify({'message': 'User deleted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# авторизация
@app.route('/login', methods=['POST'])
def login():
    try:
        # Получение данных из запроса
        login_data = request.json
        email = login_data['email']
        password = login_data['password']

        # Открытие соединения с базой данных
        with sqlite3.connect('restaurant.db') as conn:
            cur = conn.cursor()

            # Поиск пользователя по email и password
            cur.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
            user = cur.fetchone()

            if user is None:
                return jsonify({'error': 'Invalid email or password'}), 401

            # Формирование объекта пользователя с дополнительным полем "authorized"
            user_data = {
                'id': user[0],
                'name': user[1],
                'email': user[2],
                'password': user[3],
                'role': user[4],
                'authorized': True
            }

        return jsonify(user_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 400
# {
#   "email": "example@example.com",
#   "password": "password123"
# }




                # заказыуууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууу


# # Удаление заказа по его ID
# @app.route('/order/<int:order_id>', methods=['POST'])
# def delete_order(order_id):
#     conn = sqlite3.connect('restaurant.db')
#     cur = conn.cursor()

#     # Проверяем, существует ли заказ с указанным ID
#     cur.execute("SELECT id FROM orders WHERE id = ?", (order_id,))
#     existing_order = cur.fetchone()

#     if existing_order:
#         # Удаляем заказ из таблицы
#         cur.execute("DELETE FROM orders WHERE id = ?", (order_id,))
#         conn.commit()
#         conn.close()
#         return jsonify({'message': 'Order deleted successfully'})
#     else:
#         conn.close()
#         return jsonify({'message': 'Order not found'})
    

# Создание нового заказа
@app.route('/order', methods=['POST'])
def create_order():
    conn = sqlite3.connect('restaurant.db')
    cur = conn.cursor()

    # Получаем данные заказа из тела запроса
    order_data = request.get_json()

    # Извлекаем необходимые поля из данных заказа
    user_id = order_data['user_id']
    address = order_data['address']
    time = order_data['time']
    dish_list = order_data['list']
    status = order_data.get('status', 'created')  # Получаем значение статуса заказа, если оно указано, иначе используем значение по умолчанию "created"
    phone = order_data.get('phone')

    # Проверяем, существует ли пользователь с указанным ID
    cur.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    existing_user = cur.fetchone()

    if existing_user:
        # Вставляем новый заказ в таблицу "orders" с пометкой is_deleted = 0 и статусом "created"
        cur.execute("INSERT INTO orders (user_id, address, time, dishList, is_deleted, status, phone) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (user_id, address, time, json.dumps(dish_list), 0, status, phone))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Order created successfully'})
    else:
        conn.close()
        return jsonify({'message': 'User not found'})
# cur.execute("INSERT INTO orders (id, user_id, address, time, dishList, is_deleted, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
#             (1, 1, "Some address", "Some time", json.dumps([
#                 {
#                     "id": 1,
#                     "value": 2
#                 },
#                 {
#                     "id": 2,
#                     "value": 3
#                 },
#                 {
#                     "id": 3,
#                     "value": 1
#                 }
#             ]), 0, "pending"))

# получение всех элементов

@app.route('/orders', methods=['GET'])
def get_orders():
    conn = sqlite3.connect('restaurant.db')
    cur = conn.cursor()

    # Получаем все неудаленные заказы из таблицы "orders"
    cur.execute("SELECT * FROM orders", ())
    orders = cur.fetchall()

    conn.close()

    if orders:
        orders_list = []
        for order in orders:
            order_data = {
                'id': order[0],
                'user_id': order[1],
                'address': order[2],
                'time': order[3],
                'dish_list': json.loads(order[4]),
                'is_deleted': order[5],
                'status': order[6],
                'phone': order[7]
            }
            orders_list.append(order_data)

        return jsonify({'orders': orders_list})
    else:
        return jsonify({'message': 'No orders found'})



# Получение информации о заказе по ID пользователя
@app.route('/order/user/<int:user_id>', methods=['GET'])
def get_order_by_user(user_id):
    conn = sqlite3.connect('restaurant.db')
    cur = conn.cursor()

    # Получаем информацию о заказах пользователя из таблицы "orders" без удаленных заказов
    cur.execute("SELECT * FROM orders WHERE user_id = ? AND is_deleted = 0", (user_id,))
    orders = cur.fetchall()

    if orders:
        response = []
        for order in orders:
            # Разбираем JSON-строку в список блюд
            dish_list = json.loads(order[4])

            # Формируем информацию о заказе в формате JSON
            order_data = {
                "id": order[0],
                "user_id": order[1],
                "address": order[2],
                "time": order[3],
                "list": dish_list,
                "status": order[6],
                "phone": order[7]
            }
            response.append(order_data)

        conn.close()
        return jsonify(response)
    else:
        conn.close()
        return jsonify({'message': 'No orders found for the user'})



# удаление заказа
@app.route('/order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    conn = sqlite3.connect('restaurant.db')
    cur = conn.cursor()

    # Получаем информацию о заказе по ID
    cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    order = cur.fetchone()

    if order:
        # Устанавливаем флаг is_deleted в 1 для мягкого удаления заказа
        cur.execute("UPDATE orders SET is_deleted = 1 WHERE id = ?", (order_id,))
        conn.commit()

        conn.close()
        return jsonify({'message': 'Order soft-deleted successfully'})
    else:
        conn.close()
        return jsonify({'message': 'Order not found'})









############################################################### корзина

# Метод для добавления элемента в таблицу "cart" с автоматической установкой даты создания
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    user_id = data.get('user_id')
    dish_id = data.get('dish_id')
    quantity = data.get('quantity')
    
    conn = sqlite3.connect('restaurant.db')
    cur = conn.cursor()
    
    # Проверка наличия пользователя и его статуса is_deleted
    cur.execute("SELECT * FROM cart WHERE user_id = ? AND is_deleted = 0", (user_id,))
    existing_user = cur.fetchone()
    
    if existing_user:
        # Получение текущего dish_list пользователя
        cur.execute("SELECT dish_list FROM cart WHERE user_id = ? AND is_deleted = 0", (user_id,))
        current_dish_list = cur.fetchone()[0]
        
        # Преобразование текущего dish_list из JSON
        current_dish_list_dict = json.loads(current_dish_list)
        
        # Проверка наличия dish_id в текущем dish_list
        if any(dish['dish_id'] == dish_id for dish in current_dish_list_dict):
            for dish in current_dish_list_dict:
                if dish['dish_id'] == dish_id:
                    dish['quantity'] += quantity
        else:
            current_dish_list_dict.append({"dish_id": dish_id, "quantity": quantity})
        
        new_dish_list_json = json.dumps(current_dish_list_dict)
        
        # Обновление dish_list для пользователя
        cur.execute("UPDATE cart SET dish_list = ? WHERE user_id = ? AND is_deleted = 0", (new_dish_list_json, user_id))
    
    else:
        # Создание нового элемента в корзине для пользователя
        new_dish_list = [{"dish_id": dish_id, "quantity": quantity}]
        new_dish_list_json = json.dumps(new_dish_list)
        
        cur.execute("INSERT INTO cart (user_id, dish_list) VALUES (?, ?)", (user_id, new_dish_list_json))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Элемент успешно добавлен в корзину'})

# Метод для получения всех записей из таблицы "cart"
@app.route('/get_all_cart_items', methods=['GET'])
def get_all_cart_items():
    conn = sqlite3.connect('restaurant.db')
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM cart")
    rows = cur.fetchall()
    
    cart_items = []
    for row in rows:
        cart_item = {
            'id': row[0],
            'user_id': row[1],
            'dish_list': row[2],
            'created_at': row[3],
            'is_deleted': row[4]
        }
        cart_items.append(cart_item)
    
    conn.close()
    
    return jsonify({'cart_items': cart_items})


# {
#     "user_id": 123,
#     "dish_list": [{"dish_id": 1, "quantity": 2}, {"dish_id": 2, "quantity": 1}]
# }








# Метод для изменения или удаления элемента в корзине по user_id и is_deleted = 0
@app.route('/update_cart_item', methods=['PUT'])
def update_cart_item():
    data = request.get_json()
    user_id = data.get('user_id')
    dish_id = data.get('dish_id')
    quantity = data.get('quantity')
    deleted = data.get('deleted')
    
    conn = sqlite3.connect('restaurant.db')
    cur = conn.cursor()
    
    # Получение текущего dish_list пользователя
    cur.execute("SELECT dish_list FROM cart WHERE user_id = ? AND is_deleted = 0", (user_id,))
    current_dish_list = cur.fetchone()
    
    if current_dish_list:
        current_dish_list_dict = json.loads(current_dish_list[0])
        
        # Поиск блюда по dish_id
        found = False
        for dish in current_dish_list_dict:
            if dish['dish_id'] == dish_id:
                found = True
                if deleted == 1:
                    current_dish_list_dict.remove(dish)
                else:
                    dish['quantity'] = quantity
        
        if not found and deleted == 1:
            return jsonify({'error': 'Нет такого блюда в корзине'})
        
        new_dish_list_json = json.dumps(current_dish_list_dict)
        
        # Обновление dish_list для пользователя
        cur.execute("UPDATE cart SET dish_list = ? WHERE user_id = ? AND is_deleted = 0", (new_dish_list_json, user_id))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Элемент успешно изменен или удален в корзине'})
    
    else:
        return jsonify({'error': 'Нет предметов в корзине для данного пользователя'})

# {
#     "user_id": 2,
#     "dish_id" : 3,
#     "quantity": 2,
#     "ideleted": 0 or 1
# } 



# Метод для удаления элемента из корзины по id
@app.route('/delete_cart_item/<int:item_id>', methods=['PUT'])
def delete_cart_item(item_id):
    conn = sqlite3.connect('restaurant.db')
    cur = conn.cursor()
    
    # Обновление поля is_deleted для элемента корзины по id
    cur.execute("UPDATE cart SET is_deleted = 1 WHERE id = ?", (item_id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Элемент успешно удален из корзины'})

# Метод для получения полной информации о корзине по user_id и is_deleted = 0
@app.route('/get_cart_items/<int:user_id>', methods=['GET'])
def get_cart_items(user_id):
    conn = sqlite3.connect('restaurant.db')
    cur = conn.cursor()
    
    # Получение полной информации о корзине пользователя с указанным user_id и is_deleted = 0
    cur.execute("SELECT * FROM cart WHERE user_id = ? AND is_deleted = 0", (user_id,))
    cart_items = cur.fetchone()
    
    conn.close()
    
    if cart_items:
        # Преобразование строки JSON в объекты Python
        cart_items_dict = {
            'id': cart_items[0],
            'user_id': cart_items[1],
            'dish_list': json.loads(cart_items[2].replace("\\", "")),
            'created_at': cart_items[3],
            'is_deleted': cart_items[4]
        }
        return jsonify({'cart_items': cart_items_dict})
    else:
        return jsonify({'message': 'Корзина пуста или не найдена'})

if __name__ == '__main__':
    app.run(debug=True)
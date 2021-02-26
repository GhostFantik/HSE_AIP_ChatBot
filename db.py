import sqlite3 as sq
import dotenv
import os
from typing import Optional
from models import Order, Product

con: sq.Connection


def connect():
    """Подключиться к бд"""
    global con
    dotenv.load_dotenv()
    try:
        con = sq.connect(os.getenv('DB'), check_same_thread=False)
        con.row_factory = sq.Row
        print('Соединение с базой данных установлено!')
    except sq.Error as e:
        if con:
            con.rollback()
            print('Ошибка подключения к базе данных!')
            print(e)


def disconnect():
    """Отключиться от бд"""
    if con:
        con.commit()
        con.close()
        print('Соединение с базой данных разорвано!')


def create_db():
    """Создать таблицы в бд"""
    try:
        cur = con.cursor()
        cur.executescript("""CREATE TABLE IF NOT EXISTS orders (
                            id INTEGER PRIMARY KEY,
                            user TEXT NOT NULL,
                            address TEXT,
                            source TEXT NOT NULL,
                            ready INTEGER DEFAULT 0);
                            CREATE TABLE IF NOT EXISTS products (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            description TEXT,
                            consist TEXT,
                            tag TEXT,
                            price INTEGER);
                            CREATE TABLE IF NOT EXISTS orders_products (
                            order_id INTEGER NOT NULL,
                            product_id INTEGER NOT NULL,
                            amount INTEGER NOT NULL DEFAULT 1,
                            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE)
                            """)
        con.commit()
    except sq.Error as e:
        if con:
            con.rollback()
        print('Ошибка выполнения запроса!')
        print(e)


def get_all_products() -> list[Product]:
    """Метод, возвращает list объектов Product. Получение всех Product из бд"""
    try:
        cur = con.cursor()
        data = cur.execute('SELECT * FROM products')
        output = []
        for d in data:
            output.append(Product(d['name'], d['description'], d['consist'], d['tag'], d['price'], _id=d['id']))
        return output
    except BaseException as e:
        if con:
            con.rollback()
        print('Ошибка выполнения запроса!')
        print(e)


def get_all_roll() -> list[Product]:
    """Метод, возвращает list объектов Product. Получение всех Product with type roll из бд"""
    try:
        cur = con.cursor()
        data = cur.execute('SELECT * FROM products WHERE tag LIKE \'roll\'')
        output = []
        for d in data:
            output.append(Product(d['name'], d['description'], d['consist'], d['tag'], d['price'], _id=d['id']))
        return output
    except BaseException as e:
        if con:
            con.rollback()
        print('Ошибка выполнения запроса!')
        print(e)


def get_all_pizza() -> list[Product]:
    """Метод, возвращает list объектов Product. Получение всех Product with type pizza из бд"""
    try:
        cur = con.cursor()
        data = cur.execute('SELECT * FROM products WHERE tag LIKE \'pizza\'')
        output = []
        for d in data:
            output.append(Product(d['name'], d['description'], d['consist'], d['tag'], d['price'], _id=d['id']))
        return output
    except BaseException as e:
        if con:
            con.rollback()
        print('Ошибка выполнения запроса!')
        print(e)


def get_product_by_name(name: str) -> Product:
    """Метод, возвращает Product по его name"""
    try:
        cur = con.cursor()
        p = cur.execute(f'SELECT * FROM products WHERE name LIKE \'{name}\'').fetchone()
        return Product(p['name'], p['description'], p['consist'], p['tag'], p['price'], _id=p['id'])
    except sq.Error as e:
        if con:
            con.rollback()
            print('Ошибка выполнения запроса!')
            print(e)


# db.add_order(Order('Egor', 'Moscow', 'vk', [('Пицца 1', 2), ('Пицца 3', 5)]))
def add_order(order: Order) -> None:
    """Добавить новый Order"""
    products_ids = []
    try:
        cur = con.cursor()
        for p in order.products:
            products_ids.append((cur.execute(f'SELECT id FROM products WHERE name LIKE \'{p[0]}\'').fetchone()['id'],
                                 p[1]))
        last_id_order = cur.execute('INSERT INTO orders VALUES (NULL, ?, ?, ?, ?)', (order.user, order.address,
                                                                                     order.source,
                                                                                     int(order.ready))).lastrowid
        for i in products_ids:
            cur.execute('INSERT INTO orders_products VALUES (?, ?, ?)', (last_id_order, i[0], i[1]))
        con.commit()
    except sq.Error as e:
        if con:
            con.rollback()
            print('Ошибка выполнения запроса!')
            print(e)


def get_order_by_user(user: str) -> Optional[Order]:
    """Получить заказ по user"""
    try:
        cur = con.cursor()
        o = cur.execute(f'SELECT * FROM orders WHERE user LIKE \'{user}\'').fetchall()
        if o:
            o = o[-1]
            return Order(user=o['user'], address=o['address'], source=o['source'], ready=o['ready'], _id=o['id'],
                         products=None)
        else:
            return None
    except sq.Error as e:
        if con:
            con.rollback()
            print('Ошибка выполнения запроса! ' + get_order_by_user.__name__)
            print(e)


def set_order_products(order: Order) -> None:
    try:
        cur = con.cursor()
        for p in order.products:
            product_id = cur.execute(f'SELECT id FROM products WHERE name LIKE \'{p[0].title()}\'').fetchone()['id']
            cur.execute('INSERT INTO orders_products VALUES (?, ?, ?)', (order.id, product_id, p[1]))
        cur.execute(f'UPDATE orders SET ready = 1 WHERE id = {order.id}')
        con.commit()
    except sq.Error as e:
        if con:
            con.rollback()
            print('Ошибка выполнения запроса! ' + get_order_by_user.__name__)
            print(e)


def set_order_address(order: Order):
    try:
        cur = con.cursor()
        cur.execute(f'UPDATE orders SET address = \'{order.address}\', ready = {order.ready} WHERE id = {order.id}')
        con.commit()
    except sq.Error as e:
        if con:
            con.rollback()
            print('Ошибка выполнения запроса! ' + get_order_by_user.__name__)
            print(e)
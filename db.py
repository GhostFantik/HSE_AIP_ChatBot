import sqlite3 as sq
import dotenv, os
from models import Order, Product

con: sq.Connection


def connect():
    global con
    dotenv.load_dotenv()
    try:
        con = sq.connect(os.getenv('DB'))
        con.row_factory = sq.Row
        print('Соединение с базой данных установлено!')
    except sq.Error as e:
        if con:
            con.rollback()
            print('Ошибка подключения к базе данных!')
            print(e)


def disconnect():
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
                            address TEXT NOT NULL,
                            source TEXT NOT NULL);
                            CREATE TABLE IF NOT EXISTS products (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            description TEXT,
                            consist TEXT,
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


def get_all_products() -> list:
    """Метод, возвращает list объектов Product. Получение всех Product из бд"""
    try:
        cur = con.cursor()
        data = cur.execute('SELECT * FROM products')
        output = []
        for d in data:
            output.append(Product(d['name'], d['description'], d['consist'], d['price'], _id=d['id']))
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
        return Product(p['name'], p['description'], p['consist'], p['price'], _id=p['id'])
    except sq.Error as e:
        if con:
            con.rollback()
            print('Ошибка выполнения запроса!')
            print(e)


# db.add_order(Order('Egor', 'Moscow', 'vk', [('Пицца 1', 2), ('Пицца 3', 5)]))
def add_order(order: Order):
    """Добавить новый Order"""
    products_ids = []
    try:
        cur = con.cursor()
        for p in order.products:
            products_ids.append((cur.execute(f'SELECT id FROM products WHERE name LIKE \'{p[0]}\'').fetchone()['id'],
                                 p[1]))
        last_id_order = cur.execute('INSERT INTO orders VALUES (NULL, ?, ?, ?)', (order.user, order.address,
                                                                                  order.source)).lastrowid
        for i in products_ids:
            cur.execute('INSERT INTO orders_products VALUES (?, ?, ?)', (last_id_order, i[0], i[1]))
        con.commit()
    except sq.Error as e:
        if con:
            con.rollback()
            print('Ошибка выполнения запроса!')
            print(e)


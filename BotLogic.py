from models import Product, Order
import pymorphy2
import db
import string

morph = pymorphy2.MorphAnalyzer()


def message_handle(user: str, source: str, message: str) -> str:
    words: list[str] = message.lower().strip().split()
    normal_words: list[str] = []
    for word in words:
        try:
            p: pymorphy2.analyzer.Parse = morph.parse(word)[0]
            normal_words.append(p.normal_form)
        except BaseException as error:
            print('Error ', error)
    return distribute(normal_words, user, source, message)


def distribute(normal_words: list[str], user: str, source: str, raw_message: str) -> str:
    order = db.get_order_by_user(user)
    if order and order.ready != 2:
        if order.ready == 0:
            return add_order_product(order, normal_words)
        elif order.ready == 1:
            return add_order_address(order, raw_message)
    if 'ролл' in normal_words:
        return get_roll()
    elif 'пицца' in normal_words:
        return get_pizza()
    elif (('оформлять' in normal_words) or ('оформить' in normal_words)) and ('заказ' in normal_words):
        return add_order_empty(user, source)
    else:
        names = [i.lower() for i in get_product_names()]
        for name in names:
            if name in normal_words:
                return get_product_info(name)


def add_order_product(order: Order, normal_words: list[str]) -> str:
    order.products = []
    names = [i.lower() for i in get_product_names()]
    for idx, word in enumerate(normal_words):
        if word in names:
            if idx < len(normal_words)-1 and normal_words[idx+1].isdigit():
                order.products.append((word, normal_words[idx+1]))
            else:
                order.products.append((word, 1))
    order.ready = 1
    db.set_order_products(order)
    return 'Введите адрес доставки:'


def add_order_address(order: Order, raw_message: str) -> str:
    order.address = raw_message
    db.set_order_address(order)
    return 'Заказ оформлен!'


def add_order_empty(user: str, source: str) -> str:
    order = Order(user=user, address=None, source=source, products=[], ready=False)
    db.add_order(order)
    return 'Введите продукты в данном формате:\nНазвание Количество Название Количество'


def get_product_names() -> list[str]:
    l: list[Product] = db.get_all_products()
    names = []
    for i in l:
        names.append(i.name)
    return names


def get_roll() -> str:
    products: list[Product] = db.get_all_roll()
    s = ''
    for product in products:
        s += f'№{product.id} {product.name.title()} {product.price}р\n'
    return s


def get_pizza() -> str:
    products: list[Product] = db.get_all_pizza()
    s = ''
    for product in products:
        s += f'№{product.id} {product.name.title()} {product.price}р\n'
    return s


def get_product_info(name: str) -> str:
    product: Product = db.get_product_by_name(name.title())
    s = f'№{product.id} {product.name} {product.price}p\nОписание:\n{product.description}\nСостав:\n{product.consist}'
    return s




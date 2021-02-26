from typing import Optional


class Order:
    def __init__(self, user: str, address: Optional[str], source: str, products: Optional[list[tuple[str, int]]], ready: int,
                 _id: int = None):
        self.id: int = _id
        self.user: str = user
        self.address: Optional[str] = address
        self.source: str = source
        self.products: Optional[list[tuple[str, int]]] = products  # список кортежей вида (название продукта,
        # количество)
        self.ready: int = ready  # 0 - ожидаются продукты 1 - ожидается адрес 2 - заказ заполнен


class Product:
    def __init__(self, name: str, description: str, consist: str, tag: str, price: int, _id: int = None):
        self.id: int = _id
        self.name: str = name
        self.description: str = description
        self.consist: str = consist
        self.tag: str = tag
        self.price: int = price

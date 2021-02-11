class Order:
    def __init__(self, user: str, address: str, source: str, products: list, _id: int = None):
        self.id = _id
        self.user = user
        self.address = address
        self.source = source
        self.products = products  # список кортежей вида (название продукта, количество)


class Product:
    def __init__(self, name: str, description: str, consist: str, price: int, _id: int = None):
        self.id = _id
        self.name = name
        self.description = description
        self.consist = consist
        self.price = price
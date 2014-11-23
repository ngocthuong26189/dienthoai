from models.product import Product
import json
import ast


class Cart:
    data = {}
    products_data = None

    def __init__(self, data={}):
        self.data = json.loads(data)

    def has_product(self, product_id):
        return self.data.get(product_id) is not None

    def add(self, product_id, quantity):
        quantity += self.quantity_of(product_id) if self.has_product(product_id) else 0
        self.update(product_id, quantity)

    def update(self, product_id, quantity):
        self.data[str(product_id)] = int(quantity)

    def remove(self, product_id):
        self.data.pop(product_id)

    def quantity_of(self, product_id):
        return self.data.get(unicode(product_id))

    @property
    def jsonified_data(self):
        return json.dumps(self.data) 

    @property
    def products(self):
        if self.products_data:
            return self.products_data
        else:
            return Product.objects(id__in=self.data.keys())

    @property
    def total(self):
        total = 0

        for product in self.products:
            quantity = self.data.get(unicode(product.id))
            total += product.price * quantity

        return total
            

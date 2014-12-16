from models.product import Product
import ast
import json


class Cart:
    data = {}

    def __init__(self, data):
        self.data = data

    def has_product(self, product_id):
        return self.products_data.get(product_id) is not None

    def add(self, product_id, quantity):
        quantity += self.quantity_of(product_id) if self.has_product(product_id) else 0
        self.update(product_id, quantity)

    def update(self, product_id, quantity):
        data = self.products_data
        data[str(product_id)] = int(quantity)
        self.data['products'] = data

    def remove(self, product_id):
        data = self.products_data
        data.pop(product_id)
        self.data["products"] = data

    def quantity_of(self, product_id):
        return self.data['products'].get(unicode(product_id))

    def update_shipping(self, shipping_data):
        self.data['shipping'] = shipping_data

    def to_order_data(self):
        products_data = self.products_data
        shipping_data = self.shipping_data

        return {
            'state': 'pending',
            'shipping_method': shipping_data['shipping_method'],
            'payment_method': shipping_data['payment_method'],
            'customer_name': shipping_data['customer_name'],
            'customer_phone': shipping_data['customer_phone'],
            'customer_email': shipping_data['customer_email'],
            'customer_city': shipping_data['customer_city'],
            'customer_address': shipping_data['customer_address'],
            'customer_remark': shipping_data['customer_remark'],
        }

    @property
    def jsonified_data(self):
        return json.dumps(self.data) 

    @property
    def shipping_data(self):
        return self.data.get('shipping', {})

    @property
    def products(self):
        return Product.objects(id__in=self.products_data.keys())

    @property
    def products_data(self):
        return self.data.get('products', {})

    @property
    def total(self):
        total = 0

        for product in self.products:
            quantity = self.data['products'].get(unicode(product.id))
            total += product.price * quantity

        return total
            

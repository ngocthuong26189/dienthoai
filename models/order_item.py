from mongoengine import *


class OrderItem(Document):
    order = ReferenceField('Order', required=True)
    product = ReferenceField('Product', required=True)
    price = IntField(min_value=0, default=0)
    quantity = IntField(min_value=1, default=1)
    

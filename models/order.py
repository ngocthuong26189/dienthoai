from mongoengine import *


class Order(Document):
    user = ReferenceField('User', required=True, reverse_delete_rule=NULLIFY)
    state = StringField()
    shipping_method = StringField()
    cod_code = StringField()
    cod_cost = IntField(min_value=0, default=0)
    cod_billing_cost = IntField(min_value=0, default=0)

def get_pending():
    return Order.objects(state='pending')

def get_complete():
    return Order.object(state='complete')

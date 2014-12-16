from mongoengine import *


class Order(Document):
    # user = ReferenceField('User', required=True, reverse_delete_rule=NULLIFY)
    state = StringField(default='pending')
    shipping_method = StringField(required=True, default='pickup')
    payment_method = StringField(required=True, default='cash_on_delivery')
    cod_code = StringField()
    cod_cost = IntField(min_value=0, default=0)
    cod_billing_cost = IntField(min_value=0, default=0)
    customer_name = StringField(required=True)
    customer_phone = StringField(required=True)
    customer_email = StringField(required=True)
    customer_city = StringField(required=True)
    customer_address = StringField(required=True)
    customer_remark = StringField()

def get_pending():
    return Order.objects(state='pending')

def get_complete():
    return Order.object(state='complete')

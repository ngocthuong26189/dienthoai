from mongoengine import *
from datetime import datetime


class Chat(Document):
    time = DateTimeField(datetime.utcnow())
    message = StringField(required=True)
    employee = ReferenceField("User",required=True)
    customer = ReferenceField("User")
    customer_name = StringField(required=True)
    

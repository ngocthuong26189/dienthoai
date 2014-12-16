from mongoengine import *
from datetime import datetime

class StaticPage(Document):
    name = StringField(required=True)
    content = StringField(required=True)
    created_at = DateTimeField(required=True, default=datetime.utcnow)
    updated_at = DateTimeField(required=True, default=datetime.utcnow)
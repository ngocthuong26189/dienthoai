from mongoengine import *
from datetime import datetime

class Comment(Document):
    topic = ObjectIdField(required=True)
    content = StringField(required=True)
    userId = ReferenceField('User',required=True)
    created_at = DateTimeField(required=True, default=datetime.utcnow)
    updated_at = DateTimeField(required=True, default=datetime.utcnow)


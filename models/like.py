from mongoengine import *
from datetime import datetime

class Like(Document):
    topic = ObjectIdField(required=True)
    user = ReferenceField("User", required=True, reverse_delete_rule=CASCADE)


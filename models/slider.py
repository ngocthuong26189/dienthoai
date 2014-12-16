from mongoengine import *

class Slider(Document):
    name = StringField(required=True)
    description = StringField()
from mongoengine import *


class Image(Document):
    original = FileField()
    thumbnail = FileField()

from mongoengine import *
from services.image import image_url
import md5


class Brand(Document):
    uid = SequenceField()
    name = StringField(required=True)
    image = StringField()
    
    @property
    def image_url(self):
        return image_url(self.image)

def get(uid):
    return Brand.objects(uid=uid).first()

def create(brand_dict):
    name = brand_dict.get('name', 'Apple')
    image = brand_dict.get('image', 'apple-logo.png')
    return Brand(name=name, image=image).save()


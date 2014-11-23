from mongoengine import *
from services.image import image_url, image_original_url


class Question_Category(Document):
    name = StringField(required=True)
    image = StringField()
    
    @property
    def image_url(self):
        if self.image is None:
            return ""
        return image_url(self.image)

    @property
    def image_original_url(self):
        if self.image is None:
            return ""
        return image_original_url(self.image)

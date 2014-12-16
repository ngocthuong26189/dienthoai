from mongoengine import *
from services.image import image_url, image_original_url
from models.slider import Slider

class Banner(Document):
    name = StringField(required=True)
    image = StringField()
    html = StringField()
    slider = ReferenceField('Slider', reverse_delete_rule=NULLIFY)
    position = StringField()
    
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

    
def get_list_position():
    return ["Top","Left","Right","Bottom"]
from mongoengine import *
from services.image import image_url, image_original_url

class Category(Document):
    name = StringField(required=True, unique=True)
    parent = ReferenceField('Category', reverse_delete_rule=NULLIFY)
    image = StringField()
    ancestors = ListField(ReferenceField('Category'))
    
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

def create(category_dict):
    name = user_dict.get('name')
    parent = user_dict.get('parent')
    image = user_dict.get('image')
    ancestors = user_dict.get('ancestors')
    return User(name=name, parent=parent, image=image, ancestors=ancestors).save()
from mongoengine import *
from services.image import image_url, image_original_url

class Category(Document):
    name = StringField(required=True, unique=True)
    parent = ReferenceField('Category', reverse_delete_rule=NULLIFY)
    image = StringField()
    ancestors = ListField(ReferenceField('Category'))
    link = StringField(required=True, unique=True)

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
    
    def get_childs(self):
        return Category.objects(parent = self.id)

    def get_level(self):
        def check_level(le,category):
                if category is not None:
                    if category.parent is None:
                        return le
                else:
                    return le
                return check_level(le+1,category.parent)
        if self.parent is None:
            return 0;
        return check_level(0, self)
        
    def get_root(self):
        def get_parrent(category):
            if category is not None:
                if category.parent is None:
                    return category
            else:
                return category
            return get_parrent(category.parent)
        return get_parrent(self)
from mongoengine import *
from services.image import image_url, image_original_url


class Product(Document):
    name = StringField(required=True)
    sku = StringField(required=True)
    image = StringField()
    category = ReferenceField('Category',required=True, reverse_delete_rule=NULLIFY)
    brand = ReferenceField('Brand', reverse_delete_rule=NULLIFY)
    price = IntField(min_value=0, default=0)
    selling_price = FloatField(min_value=0, default=0)
    discount = FloatField(min_value=0, max_value=100, default=0)

    @property
    def slug(self):
        return "{0}:slug-to-update-later".format(self.id)

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

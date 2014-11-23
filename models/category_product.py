from mongoengine import *


class Category_Product(Document):
    product = ReferenceField("Product", required=True, reverse_delete_rule=CASCADE)
    category = ReferenceField('Category',required=True, reverse_delete_rule=CASCADE)
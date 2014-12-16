from models.category import Category
from models.product import Product
from models.category_product import Category_Product


def rebuilt_category_product():
    Category_Product.objects().delete()
    categories = Category.objects()
    for category in categories:
        product_of_categorys = Product.objects(category=category.id)
        bulk = []
        for product_of_category in product_of_categorys:
            bulk.append(Category_Product(product=product_of_category.id,category=category.id))
        if len(bulk) > 0: 
           Category_Product.objects.insert(bulk)
        children = Category.objects(ancestors__contains=category.id)
        for child in children:
            product_of_childs = Product.objects(category=child.id)
            bulk = []
            for product_of_child in product_of_childs:
                bulk.append(Category_Product(product=product_of_child.id,category=category.id))
            if len(bulk) > 0:
                Category_Product.objects.insert(bulk)
def get_child_category(category_id):
    # childs = []
    # category = Category.objects(id=str(category_id)).first()
    # if category is None:
    #     return childs
    parent = Category.objects.get(parent = category.id)
    return parent
from flask import Blueprint
from flask import render_template as render
from services.paginate import Paginate
from models.product import Product


module = Blueprint('site_product', __name__)

@module.route('/')
def index():
    pagination = Paginate('sites_product.index', count=len(Product.objects), per_page=10)
    page = pagination.get_page()
    products = Product.objects[(page-1) * 10:page * 10]
    return render('sites/product/index.html', products=products, page=page, pagination=pagination)


@module.route('/<string:product_slug>', methods=['GET'])
def detail(product_slug):
    product_id = product_slug.split(':')[0]
    product = Product.objects(id=str(product_id)).first()
    return render('sites/product/detail.html', product=product)



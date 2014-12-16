from flask import Blueprint
from flask import request, abort
from models.product import Product
from models.category import Category
from models.brand import Brand
from services import render
from mongoengine import *
from services.paginate import Paginate
from services.cache import rebuilt_category_product

module = Blueprint('admin.product', __name__)

@module.route('/')
def index():
    # Slice of to pagination

    # List of filter by get args:
    # Example: /admin/product/?page=1&name_icontains=dolot&category__icontains=treem
    data = request.args.to_dict()

    # Type of filter
    engine_filter = {'name__icontains': str, 'category__icontains': str}

    # Prepare filter
    criteria = {}
    for k in data:
        if k in engine_filter:
            criteria[k] = engine_filter[k](data[k])

    pagination = Paginate('admin.product.index', count=len(Product.objects(**criteria)), per_page=10)
    page = pagination.get_page()
    products = Product.objects(**criteria)[(page-1) * 10:page * 10]
    return render.template('admin/product/index.html', products=products, pagination=pagination)

@module.route('/<string:product_id>', methods=['GET'])
def detail(product_id):
    try:
        product = Product.objects.get(id=product_id)
        return render.template('admin/product/detail.html', product=product)
    except Exception:
        abort(404)

@module.route('/', methods=['POST'])
def create():
    try:
        data = request.form.to_dict()
        data = dict((k, v) for (k, v) in data.iteritems() if len(str(v).strip())>0)
        if 'category' in data:
            data['category'] = Category.objects.get(id = str(data['category']))
        if 'brand' in data:
            data['brand'] = Brand.objects.get(id = str(data['brand']))    
        product = Product.objects.create(**data)
        rebuilt_category_product()
        return render.template('admin/product/detail.html', product=product), 201
    except ValidationError as ve:
        abort(400, "Validation Error")
    except Exception:
        abort(400, 'Validation Error')

@module.route('/create', methods=['GET'])
def add():
    categories = Category.objects()
    brands = Brand.objects()
    return render.template('admin/product/create.html',categories=categories,brands=brands)

@module.route('/<string:product_id>/edit', methods=['GET'])
def edit(product_id):
    try:
        product = Product.objects.get(id=product_id)
        categories = Category.objects()
        brands = Brand.objects()
        return render.template('admin/product/edit.html', product=product,categories=categories,brands=brands)
    except DoesNotExist:
        abort(404, "404 does not exist")

@module.route('/<string:product_id>/update', methods=['POST'])
def update(product_id):
    try:
        data = request.form.to_dict()
        temp_data = data
        data = dict((k, v) for (k, v) in data.iteritems() if len(str(v).strip())>0)
        update_map = dict([('set__' + key, value) for key, value in data.items()])

        if update_map.has_key('set__category'):
            update_map['set__category'] = Category.objects.get(id=str(update_map['set__category']))
            if update_map['set__category'] is None:
                raise ValidationError("Category not found")

        if update_map.has_key('set__brand'):
            update_map['set__brand'] = Brand.objects.get(id=str(update_map['set__brand']))
            if update_map['set__brand'] is None:
                raise ValidationError("Brand not found")

        product = Product.objects.get(id=product_id)

        if temp_data.has_key('brand'):
            if len(str(temp_data['brand']).strip()) == 0:
                update_map['set__brand'] = None

        if temp_data.has_key('images[]'):
            update_map.pop('set__images[]')
            update_map['set__images'] = request.form.getlist('images[]')
        # print update_map
        product.update(**update_map)
        product.reload()
        rebuilt_category_product()
        return render.template('admin/product/detail.html', product=product)
    except DoesNotExist:
        abort(404, "Does Not Exist")
    except ValidationError as ve:
        abort(404, "Validation error")
    except Exception:
        abort(404, 'ValueError Error')

@module.route('/<string:product_id>/delete', methods=['POST'])
def delete(product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        return render.template('admin/product/detail.html', product=product), 200
    except Exception:
        abort(404)


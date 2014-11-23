from flask import Blueprint
from flask import request, abort
from models.brand import Brand
from services import render
from services.image import image_url
from mongoengine import *
from services.paginate import Paginate


module = Blueprint('admin.brand', __name__)

@module.route('/')
def index():
    # Slice of to pagination

    # List of filter by get args:
    # Example: /admin/brand/?page=1&name_icontains=apple
    data = request.args.to_dict()

    # Type of filter
    engine_filter = {'name__icontains': str}

    # Prepare filter
    criteria = {}
    for k in data:
        if k in engine_filter:
            criteria[k] = engine_filter[k](data[k])

    pagination = Paginate('admin.brand.index', count=len(Brand.objects(**criteria)), per_page=10)
    page = pagination.get_page()
    brands = Brand.objects(**criteria)[(page-1) * 10:page * 10]
    return render.template('admin/brand/index.html', brands=brands, pagination=pagination)

@module.route('/<int:brand_id>', methods=['GET'])
def detail(brand_id):
    try:
        b = Brand.objects.get(uid=brand_id)
        return render.template('admin/brand/detail.html', brand=b)
    except DoesNotExist:
        abort(404)

@module.route('/', methods=['POST'])
def create():
    try:
        data = request.form.to_dict()
        brand = Brand.objects.create(**data)
        return render.template('admin/brand/detail.html', brand=brand), 201
    except ValidationError as ve:
        abort(400, "Validation Error")

@module.route('/create', methods=['GET'])
def add():
    return render.template('admin/brand/create.html')

@module.route('/<int:brand_id>/edit', methods=['GET'])
def edit(brand_id):
    try:
        b = Brand.objects.get(uid=brand_id)
        return render.template('admin/brand/edit.html', brand=b)
    except DoesNotExist:
        abort(404, "404 does not exist")

@module.route('/<int:brand_id>/update', methods=['POST'])
def update(brand_id):
    try:
        data = request.form.to_dict()
        update_map = dict([('set__' + key, value) for key, value in data.items()])
        b = Brand.objects.get(uid=brand_id)
        b.update(**update_map)
        b.reload()
        return render.template('admin/brand/detail.html', brand=b)
    except DoesNotExist:
        abort(404)
    except ValidationError as ve:
        abort(400, "Validation error")


@module.route('/<int:brand_id>/delete', methods=['POST'])
def delete(brand_id):
    try:
        b = Brand.objects.get(uid=brand_id)
        b.delete()
        return render.template('admin/brand/detail.html', brand=b)
    except DoesNotExist:
        abort(404)


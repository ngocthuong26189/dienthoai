from flask import Blueprint
from flask import request, abort
from models.sticky import Sticky
from services import render
from mongoengine import *
from services.paginate import Paginate


module = Blueprint('admin.sticky', __name__)

@module.route('/')
def index():
    # Slice of to pagination

    # List of filter by get args:
    # Example: /admin/sticky/?page=1&name_icontains=apple
    data = request.args.to_dict()

    # Type of filter
    engine_filter = {'name__icontains': str}

    # Prepare filter
    criteria = {}
    for k in data:
        if k in engine_filter:
            criteria[k] = engine_filter[k](data[k])

    pagination = Paginate('admin.sticky.index', count=len(Sticky.objects(**criteria)), per_page=10)
    page = pagination.get_page()
    stickys = Sticky.objects(**criteria)[(page-1) * 10:page * 10]
    return render.template('admin/sticky/index.html', stickys=stickys, pagination=pagination)

@module.route('/<string:sticky_id>', methods=['GET'])
def detail(sticky_id):
    try:
        b = Sticky.objects.get(id=sticky_id)
        return render.template('admin/sticky/detail.html', sticky=b)
    except Exception:
        abort(404)

@module.route('/', methods=['POST'])
def create():
    try:
        data = request.form.to_dict()
        data = dict((k, v) for (k, v) in data.iteritems() if len(str(v).strip())>0)
        sticky = Sticky.objects.create(**data)
        return render.template('admin/sticky/detail.html', sticky=sticky), 201
    except ValidationError as ve:
        abort(400, "Validation Error")

@module.route('/create', methods=['GET'])
def add():
    return render.template('admin/sticky/create.html')

@module.route('/<string:sticky_id>/edit', methods=['GET'])
def edit(sticky_id):
    try:
        b = Sticky.objects.get(id=sticky_id)
        return render.template('admin/sticky/edit.html', sticky=b)
    except DoesNotExist:
        abort(404, "404 does not exist")

@module.route('/<string:sticky_id>/update', methods=['POST'])
def update(sticky_id):
    try:
        data = request.form.to_dict()
        data = dict((k, v) for (k, v) in data.iteritems() if len(str(v).strip())>0)
        update_map = dict([('set__' + key, value) for key, value in data.items()])
        b = Sticky.objects.get(id=sticky_id)
        b.update(**update_map)
        b.reload()
        return render.template('admin/sticky/detail.html', sticky=b)
    except Exception:
        abort(404)


@module.route('/<string:sticky_id>/delete', methods=['POST'])
def delete(sticky_id):
    try:
        b = Sticky.objects.get(id=sticky_id)
        b.delete()
        return render.template('admin/sticky/detail.html', sticky=b)
    except Exception:
        abort(404)


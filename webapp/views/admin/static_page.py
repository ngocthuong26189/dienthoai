from flask import Blueprint
from flask import request, abort,session
from models.static_page import StaticPage
from services import render
from mongoengine import *
import json
from services.paginate import Paginate
from models.news_category import News_Category
from services import identity

module = Blueprint('admin.static_page', __name__)

@module.route('/')
def index():
    # Slice of to pagination

    # List of filter by get args:
    # Example: /admin/static_page/?page=1&name_icontains=apple
    data = request.args.to_dict()

    # Type of filter
    engine_filter = {'name__icontains': str}

    # Prepare filter
    criteria = {}
    for k in data:
        if k in engine_filter:
            criteria[k] = engine_filter[k](data[k])

    pagination = Paginate('admin.static_page.index', count=len(StaticPage.objects(**criteria)), per_page=10)
    page = pagination.get_page()
    static_pages = StaticPage.objects(**criteria)[(page-1) * 10:page * 10]
    return render.template('admin/static_page/index.html', static_pages=static_pages, pagination=pagination)

@module.route('/<string:static_page_id>', methods=['GET'])
def detail(static_page_id):
    try:
        b = StaticPage.objects.get(id=static_page_id)
        return render.template('admin/static_page/detail.html', static_page=b)
    except Exception:
        abort(404)

@module.route('/', methods=['POST'])
def create():
    try:
        data = request.form.to_dict()
        data = dict((k, v) for (k, v) in data.iteritems() if len(str(v).strip())>0)
        static_page = StaticPage.objects.create(**data)
        return render.template('admin/static_page/detail.html', static_page=static_page), 201
    except ValidationError as ve:
        abort(400, "Validation Error")

@module.route('/create', methods=['GET'])

def add():
    return render.template('admin/static_page/create.html')

@module.route('/<string:static_page_id>/edit', methods=['GET'])

def edit(static_page_id):
    try:
        b = StaticPage.objects.get(id=static_page_id)
        return render.template('admin/static_page/edit.html', static_page=b)
    except DoesNotExist:
        abort(404, "404 does not exist")

@module.route('/<string:static_page_id>/update', methods=['POST'])
def update(static_page_id):
    try:
        data = request.form.to_dict()
        data = dict((k, v) for (k, v) in data.iteritems() if len(str(v).strip())>0)
        update_map = dict([('set__' + key, value) for key, value in data.items()])
        b = StaticPage.objects.get(id=static_page_id)
        b.update(**update_map)
        b.reload()
        return render.template('admin/static_page/detail.html', static_page=b)
    except Exception as e:
        abort(404)


@module.route('/<string:static_page_id>/delete', methods=['POST'])
def delete(static_page_id):
    try:
        b = StaticPage.objects.get(id=static_page_id)
        b.delete()
        return render.template('admin/static_page/detail.html', static_page=b)
    except Exception:
        abort(404)


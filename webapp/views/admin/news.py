from flask import Blueprint
from flask import request, abort,session
from models.news import News
from services import render
from mongoengine import *
import json
from services.paginate import Paginate
from models.news_category import News_Category
from services import identity

module = Blueprint('admin.news', __name__)

@module.route('/')
def index():
    # Slice of to pagination

    # List of filter by get args:
    # Example: /admin/news/?page=1&name_icontains=apple
    data = request.args.to_dict()

    # Type of filter
    engine_filter = {'title__icontains': str}

    # Prepare filter
    criteria = {}
    for k in data:
        if k in engine_filter:
            criteria[k] = engine_filter[k](data[k])

    pagination = Paginate('admin.news.index', count=len(News.objects(**criteria)), per_page=10)
    page = pagination.get_page()
    newss = News.objects(**criteria)[(page-1) * 10:page * 10]
    return render.template('admin/news/index.html', newss=newss, pagination=pagination)

@module.route('/<string:news_id>', methods=['GET'])
def detail(news_id):
    try:
        b = News.objects.get(id=news_id)
        return render.template('admin/news/detail.html', news=b)
    except Exception:
        abort(404)

@module.route('/', methods=['POST'])
@identity.permission_required(2)
def create():
    try:
        data = request.form.to_dict()
        data = dict((k, v) for (k, v) in data.iteritems() if len(str(v).strip())>0)
        data['author'] = json.loads(session.get('user')).get('_id').get('$oid')
        news = News.objects.create(**data)
        return render.template('admin/news/detail.html', news=news), 201
    except ValidationError as ve:
        abort(400, "Validation Error")

@module.route('/create', methods=['GET'])
@identity.permission_required(2)
def add():
    categories = News_Category.objects()
    username=json.loads(session.get('user')).get('username')
    return render.template('admin/news/create.html',categories=categories, username=username)

@module.route('/<string:news_id>/edit', methods=['GET'])
@identity.permission_required(2)
def edit(news_id):
    try:
        b = News.objects.get(id=news_id)
        categories = News_Category.objects()
        username=json.loads(session.get('user')).get('username')
        if str(b.author.id) != str(json.loads(session.get('user')).get('_id').get('$oid')) or (str(b.author.id) != str(json.loads(session.get('user')).get('_id').get('$oid')) and json.loads(session.get('user')).get('permission') < 3):
            return abort(403)
        return render.template('admin/news/edit.html', news=b,categories=categories,username=username)
    except DoesNotExist:
        abort(404, "404 does not exist")

@module.route('/<string:news_id>/update', methods=['POST'])
@identity.permission_required(2)
def update(news_id):
    try:
        data = request.form.to_dict()
        data = dict((k, v) for (k, v) in data.iteritems() if len(str(v).strip())>0)
        if data['author']:
            del data['author']
        update_map = dict([('set__' + key, value) for key, value in data.items()])
        b = News.objects.get(id=news_id)
        b.update(**update_map)
        b.reload()
        if data.get('show_in_index') is None:
            b.show_in_index = False
            b.save()
            b.reload()
        return render.template('admin/news/detail.html', news=b)
    except Exception as e:
        abort(404)


@module.route('/<string:news_id>/delete', methods=['POST'])
def delete(news_id):
    try:
        b = News.objects.get(id=news_id)
        b.delete()
        return render.template('admin/news/detail.html', news=b)
    except Exception:
        abort(404)


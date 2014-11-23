from flask import Blueprint
from flask import request, abort
from models.question_category import Question_Category
from services import render
from mongoengine import *
from services.paginate import Paginate


module = Blueprint('admin.question_category', __name__)

@module.route('/')
def index():
    # Slice of to pagination

    # List of filter by get args:
    # Example: /admin/question_category/?page=1&name_icontains=apple
    data = request.args.to_dict()

    # Type of filter
    engine_filter = {'name__icontains': str}

    # Prepare filter
    criteria = {}
    for k in data:
        if k in engine_filter:
            criteria[k] = engine_filter[k](data[k])

    pagination = Paginate('admin.question_category.index', count=len(Question_Category.objects(**criteria)), per_page=10)
    page = pagination.get_page()
    question_categorys = Question_Category.objects(**criteria)[(page-1) * 10:page * 10]
    return render.template('admin/question_category/index.html', question_categorys=question_categorys, pagination=pagination)

@module.route('/<string:question_category_id>', methods=['GET'])
def detail(question_category_id):
    try:
        b = Question_Category.objects.get(id=question_category_id)
        return render.template('admin/question_category/detail.html', question_category=b)
    except Exception:
        abort(404)

@module.route('/', methods=['POST'])
def create():
    try:
        data = request.form.to_dict()
        data = dict((k, v) for (k, v) in data.iteritems() if len(str(v).strip())>0)
        question_category = Question_Category.objects.create(**data)
        return render.template('admin/question_category/detail.html', question_category=question_category), 201
    except ValidationError as ve:
        abort(400, "Validation Error")

@module.route('/create', methods=['GET'])
def add():
    return render.template('admin/question_category/create.html')

@module.route('/<string:question_category_id>/edit', methods=['GET'])
def edit(question_category_id):
    try:
        b = Question_Category.objects.get(id=question_category_id)
        return render.template('admin/question_category/edit.html', question_category=b)
    except DoesNotExist:
        abort(404, "404 does not exist")

@module.route('/<string:question_category_id>/update', methods=['POST'])
def update(question_category_id):
    try:
        data = request.form.to_dict()
        data = dict((k, v) for (k, v) in data.iteritems() if len(str(v).strip())>0)
        update_map = dict([('set__' + key, value) for key, value in data.items()])
        b = Question_Category.objects.get(id=question_category_id)
        b.update(**update_map)
        b.reload()
        return render.template('admin/question_category/detail.html', question_category=b)
    except Exception:
        abort(404)


@module.route('/<string:question_category_id>/delete', methods=['POST'])
def delete(question_category_id):
    try:
        b = Question_Category.objects.get(id=question_category_id)
        b.delete()
        return render.template('admin/question_category/detail.html', question_category=b)
    except Exception:
        abort(404)


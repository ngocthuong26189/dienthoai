from flask import Blueprint
from flask import request, abort,session
from models.question import Question
from services import render
from mongoengine import *
import json
from services.paginate import Paginate
from models.question_category import Question_Category
from services import identity

module = Blueprint('admin.question', __name__)

@module.route('/')
def index():
    # Slice of to pagination

    # List of filter by get args:
    # Example: /admin/question/?page=1&name_icontains=apple
    data = request.args.to_dict()

    # Type of filter
    engine_filter = {'content__icontains': str}

    # Prepare filter
    criteria = {}
    for k in data:
        if k in engine_filter:
            criteria[k] = engine_filter[k](data[k])

    pagination = Paginate('admin.question.index', count=len(Question.objects(**criteria)), per_page=10)
    page = pagination.get_page()
    questions = Question.objects(**criteria)[(page-1) * 10:page * 10]
    return render.template('admin/question/index.html', questions=questions, pagination=pagination)

@module.route('/<string:question_id>', methods=['GET'])
def detail(question_id):
    try:
        b = Question.objects.get(id=question_id)
        return render.template('admin/question/detail.html', question=b)
    except Exception:
        abort(400, 'ValueError Error')

@module.route('/', methods=['POST'])
@identity.permission_required(2)
def create():
    try:
        data = request.form.to_dict()
        data = dict((k, v) for (k, v) in data.iteritems() if len(str(v).strip())>0)
        data['user'] = json.loads(session.get('user')).get('_id').get('$oid')
        question = Question.objects.create(**data)
        return render.template('admin/question/detail.html', question=question), 201
    except ValidationError as ve:
        abort(400, "Validation Error")

@module.route('/create', methods=['GET'])
@identity.permission_required(2)
def add():
    categories = Question_Category.objects()
    username=json.loads(session.get('user')).get('username')
    return render.template('admin/question/create.html',categories=categories, username=username)

@module.route('/<string:question_id>/edit', methods=['GET'])
@identity.permission_required(2)
def edit(question_id):
    try:
        b = Question.objects.get(id=question_id)
        categories = Question_Category.objects()
        username=json.loads(session.get('user')).get('username')
        if str(b.user.id) != str(json.loads(session.get('user')).get('_id').get('$oid')) or (str(b.user.id) != str(json.loads(session.get('user')).get('_id').get('$oid')) and json.loads(session.get('user')).get('permission') < 3):
            return abort(403)
        return render.template('admin/question/edit.html', question=b,categories=categories,username=username)
    except DoesNotExist:
        abort(404, "404 does not exist")
    except Exception:
        abort(400, 'ValueError Error')

@module.route('/<string:question_id>/update', methods=['POST'])
@identity.permission_required(2)
def update(question_id):
    try:
        data = request.form.to_dict()
        data = dict((k, v) for (k, v) in data.iteritems() if len(str(v).strip())>0)
        if data['user']:
            del data['user']
        update_map = dict([('set__' + key, value) for key, value in data.items()])
        b = Question.objects.get(id=question_id)
        b.update(**update_map)
        b.reload()
        if data.get('show_in_index') is None:
            b.show_in_index = False
            b.save()
            b.reload()
        return render.template('admin/question/detail.html', question=b)
    except Exception as e:
        abort(404)


@module.route('/<string:question_id>/delete', methods=['POST'])
def delete(question_id):
    try:
        b = Question.objects.get(id=question_id)
        b.delete()
        return render.template('admin/question/detail.html', question=b)
    except Exception:
        abort(404)


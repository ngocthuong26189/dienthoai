from flask import Blueprint
from flask import request, abort
from models.user import User, generate_encrypt_password
from services import render
from mongoengine import *
from services.paginate import Paginate
from services import identity

module = Blueprint('admin.user', __name__)

@module.route('/')
def index():
    # Slice of to pagination

    # List of filter by get args:
    # Example: /admin/user/?page=1&username_icontains=duythinht&permission=3
    data = request.args.to_dict()

    # Type of filter
    engine_filter = {'username__icontains': str, 'email__icontains': str, 'permission': int}

    # Prepare filter
    criteria = {}
    for k in data:
        if k in engine_filter:
            criteria[k] = engine_filter[k](data[k])

    pagination = Paginate('admin.user.index', count=len(User.objects(**criteria)), per_page=10)
    page = pagination.get_page()
    users = User.objects(**criteria)[(page-1) * 10:page * 10]
    return render.template('admin/user/index.html', users=users, pagination=pagination)

@module.route('/<int:user_id>', methods=['GET'])
@identity.permission_required(3)
def detail(user_id):
    try:
        u = User.objects.get(uid=user_id)
        return render.template('admin/user/detail.html', user=u)
    except DoesNotExist:
        abort(404)

@module.route('/', methods=['POST'])
def create():
    try:
        data = request.form.to_dict()
        data['password'] = generate_encrypt_password(data.get('password',''))
        user = User.objects.create(**data)
        return render.template('admin/user/detail.html', user=user), 201
    except NotUniqueError as e:
        abort(400, "Duplicated, username is existed") # Duplicate
    except ValidationError as ve:
        abort(400, "Validation Error")

@module.route('/create', methods=['GET'])
def add():
    return render.template('admin/user/create.html')

@module.route('/<int:user_id>/edit', methods=['GET'])
def edit(user_id):
    try:
        u = User.objects.get(uid=user_id)
        return render.template('admin/user/edit.html', user=u)
    except DoesNotExist:
        abort(404, "404 does not exist")

@module.route('/<int:user_id>/update', methods=['POST'])
def update(user_id):
    try:
        data = request.form.to_dict()
        # Hash the password if exists
        if 'password' in data:
            data['password'] = generate_encrypt_password(data.get('password', ''))
        update_map = dict([('set__' + key, value) for key, value in data.items()])
        u = User.objects.get(uid=user_id)
        u.update(**update_map)
        u.reload()
        return render.template('admin/user/detail.html', user=u)
    except DoesNotExist:
        abort(404)
    except NotUniqueError:
        abort(400, "Duplicated, username is existed")
    except ValidationError as ve:
        abort(400, "Validation error")


@module.route('/<int:user_id>/delete', methods=['POST'])
def delete(user_id):
    try:
        u = User.objects.get(uid=user_id)
        u.delete()
        return render.template('admin/user/detail.html', user=u)
    except DoesNotExist:
        abort(404)

from flask import Blueprint
from flask import request, abort,session
from models.banner import Banner,get_list_position
from services import render
from mongoengine import *
import json
from services.paginate import Paginate
from models.slider import Slider
from services import identity
from bson.objectid import ObjectId

module = Blueprint('admin.banner', __name__)

@module.route('/')
def index():
    # Slice of to pagination

    # List of filter by get args:
    # Example: /admin/banner/?page=1&name_icontains=apple
    data = request.args.to_dict()

    # Type of filter
    engine_filter = {'name__icontains': str,'slider__icontains': str}
    # isValid
    
    criteria = {}
    for k in data:
        if k in engine_filter:
            criteria[k] = engine_filter[k](data[k])
    if criteria.has_key('slider__icontains'):
        if not ObjectId.is_valid(criteria['slider__icontains']):
            del criteria['slider__icontains']
    pagination = Paginate('admin.banner.index', count=len(Banner.objects(**criteria)), per_page=10)
    page = pagination.get_page()
    banners = Banner.objects(**criteria)[(page-1) * 10:page * 10]

    sliders = Slider.objects()
    return render.template('admin/banner/index.html', banners=banners, pagination=pagination,sliders=sliders)

@module.route('/<string:banner_id>', methods=['GET'])
def detail(banner_id):
    try:
        b = Banner.objects.get(id=banner_id)
        return render.template('admin/banner/detail.html', banner=b)
    except Exception:
        abort(404, 'ValueError Error')

@module.route('/', methods=['POST'])
def create():
    try:
        data = request.form.to_dict()
        data = dict((k, v) for (k, v) in data.iteritems() if len(str(v).strip())>0)
        banner = Banner.objects.create(**data)
        return render.template('admin/banner/detail.html', banner=banner), 201
    except ValidationError as ve:
        abort(400, "Validation Error")

@module.route('/create', methods=['GET'])
def add():
    sliders = Slider.objects()
    positions = get_list_position()
    return render.template('admin/banner/create.html',sliders=sliders,positions=positions)

@module.route('/<string:banner_id>/edit', methods=['GET'])
def edit(banner_id):
    try:
        b = Banner.objects.get(id=banner_id)
        sliders = Slider.objects()
        positions = get_list_position()
        return render.template('admin/banner/edit.html', banner=b,sliders=sliders,positions=positions)
    except DoesNotExist:
        abort(404, "404 does not exist")
    except Exception:
        abort(400, 'ValueError Error')

@module.route('/<string:banner_id>/update', methods=['POST'])
def update(banner_id):
    try:
        data = request.form.to_dict()
        data = dict((k, v) for (k, v) in data.iteritems() if len(str(v).strip())>0)
        update_map = dict([('set__' + key, value) for key, value in data.items()])
        b = Banner.objects.get(id=banner_id)
        b.update(**update_map)
        b.reload()
        return render.template('admin/banner/detail.html', banner=b)
    except Exception as e:
        abort(404)


@module.route('/<string:banner_id>/delete', methods=['POST'])
def delete(banner_id):
    try:
        b = Banner.objects.get(id=banner_id)
        b.delete()
        return render.template('admin/banner/detail.html', banner=b)
    except Exception as e:
        abort(404)


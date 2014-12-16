from flask import Blueprint
from flask import request, abort
from models.slider import Slider
from models.banner import Banner
from services import render
from mongoengine import *
from services.paginate import Paginate


module = Blueprint('admin.slider', __name__)

@module.route('/')
def index():
    # Slice of to pagination

    # List of filter by get args:
    # Example: /admin/slider/?page=1&name_icontains=apple
    data = request.args.to_dict()

    # Type of filter
    engine_filter = {'name__icontains': str}

    # Prepare filter
    criteria = {}
    for k in data:
        if k in engine_filter:
            criteria[k] = engine_filter[k](data[k])

    pagination = Paginate('admin.slider.index', count=len(Slider.objects(**criteria)), per_page=10)
    page = pagination.get_page()
    sliders = Slider.objects(**criteria)[(page-1) * 10:page * 10]
    return render.template('admin/slider/index.html', sliders=sliders, pagination=pagination)

@module.route('/<string:slider_id>', methods=['GET'])
def detail(slider_id):
    try:
        b = Slider.objects.get(id=slider_id)
        return render.template('admin/slider/detail.html', slider=b)
    except Exception:
        abort(404)

@module.route('/', methods=['POST'])
def create():
    try:
        data = request.form.to_dict()
        data = dict((k, v) for (k, v) in data.iteritems() if len(str(v).strip())>0)
        if data.get('banners') is not None:
            data['banners'] = str(data['banners']).split(',');
        slider = Slider.objects.create(**data)
        return render.template('admin/slider/detail.html', slider=slider), 201
    except Exception as ve:
        abort(400, "Validation Error")

@module.route('/create', methods=['GET'])
def add():
    try:
        return render.template('admin/slider/create.html')
    except Exception, e:
        abort(404, "404 does not exist")
    

@module.route('/<string:slider_id>/edit', methods=['GET'])
def edit(slider_id):
    try:
        b = Slider.objects.get(id=slider_id)
        return render.template('admin/slider/edit.html', slider=b)
    except DoesNotExist:
        abort(404, "404 does not exist")

@module.route('/<string:slider_id>/update', methods=['POST'])
def update(slider_id):
    try:
        data = request.form.to_dict()
        data = dict((k, v) for (k, v) in data.iteritems() if len(str(v).strip())>0)
        update_map = dict([('set__' + key, value) for key, value in data.items()])
        b = Slider.objects.get(id=slider_id)
        b.update(**update_map)
        b.reload()
        return render.template('admin/slider/detail.html', slider=b)
    except Exception:
        abort(404)


@module.route('/<string:slider_id>/delete', methods=['POST'])
def delete(slider_id):
    try:
        b = Slider.objects.get(id=slider_id)
        b.delete()
        return render.template('admin/slider/detail.html', slider=b)
    except Exception:
        abort(404)


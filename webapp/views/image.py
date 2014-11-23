from flask import Blueprint
from flask import request, abort, send_file
from models.storage import Image
from mongoengine import *
import io

module = Blueprint('image', __name__)

@module.route('/')
def index():
    return 'Not yet implements', 400

@module.route('/<object_id>/')
def show(object_id):
    return 'Not yet implements', 400

@module.route('/<object_id>/original')
def original(object_id):
    try:
        image = Image.objects.get(id=object_id)
        f = image.original
        return send_file(io.BytesIO(f.read()), attachment_filename='logo.png', mimetype=f.content_type)
    except DoesNotExist:
        abort(404)
    except ValidationError:
        abort(404)
        
@module.route('/<object_id>/thumbnail')
def thumbnail(object_id):
    try:
        image = Image.objects.get(id=object_id)
        f = image.thumbnail
        return send_file(io.BytesIO(f.read()), attachment_filename='logo.png', mimetype=f.content_type)
    except DoesNotExist:
        abort(404)
    except ValidationError:
        abort(404)
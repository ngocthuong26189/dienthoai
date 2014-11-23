from flask import Blueprint
from flask import request
from services.image import image_url
from services import render
from models.storage import Image
from PIL import Image as ImagePIL
import io


module = Blueprint('API_UPLOAD', __name__)

@module.route('/', methods=['GET'])
def index():
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="/api/v1/upload/" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
@module.route('/', methods=['POST'])
def upload():

    # Allow only image
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    f = request.files['file']

    ext = f.filename.rsplit('.', 1)[1]

    if ext in ALLOWED_EXTENSIONS:

        image_data = f.read()
        image = Image()

        image.original.put(image_data, content_type=f.content_type)

        # process for thumbnail
        stream = io.BytesIO(image_data)
        im = ImagePIL.open(stream)
        size = 200, 200
        im.thumbnail(size, ImagePIL.ANTIALIAS)

        # save the thumbnail to data
        thumb = io.BytesIO()
        im.save(thumb, 'png')
        image.thumbnail.put(thumb.getvalue(), content_type=f.content_type)

        # save data
        image.save()

        data = {
            'object_id': str(image.id),
            'original': image_url(image.id, 'original'),
            'thumbnail': image_url(image.id)
            }
        return render.json(data)
    return render.json("Invalidate file type"), 400

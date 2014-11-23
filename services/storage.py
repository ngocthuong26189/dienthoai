import cloudstorage as gcs
from google.appengine.api import app_identity
from google.appengine.api import images

from time import time
from services import system

def save_image(upload_file):

    image_data = upload_file.read()
    filename = str(time())
    ext = upload_file.filename.split('.')[-1]  #filename extentions (.png, .jpg, .docx...)

    # Make a file name like /bucket_name/12341.1232-original.png

    gcs_filename = '/%s/images/%s-original.%s' % (app_identity.get_default_gcs_bucket_name(), filename, ext)
    gcs_thumbnail_filename = '/%s/images/%s-thumbnail.%s' % (app_identity.get_default_gcs_bucket_name(), filename, ext)

    thumbnail_data = images.resize(image_data, 200, 200)

    # Write file to google cloud storage
    write_file(gcs_filename, image_data)
    write_file(gcs_thumbnail_filename, thumbnail_data)

    # Return url data
    return {'original': get_host() + gcs_filename, 'thumbnail': get_host() + gcs_thumbnail_filename}

def save_file(upload_file):

    file_data = upload_file.read()
    filename = str(time())
    ext = upload_file.filename.split('.')[-1]

    gcs_filename = '/%s/files/%s.%s' % (app_identity.get_default_gcs_bucket_name(), filename, ext)

    # Write file to google cloud storage
    with gcs.open(gcs_filename, 'w', content_type=upload_file.content_type, options={b'x-goog-acl': b'public-read'}) as gcs_file:
        gcs_file.write(file_data)

    return {'url': get_host() + gcs_filename}

# Get cdn hostname
def get_host():
    if not system.is_develop():
        return 'http://storage.googleapis.com'
    return 'http://localhost:8080/_ah/gcs'

def write_file(filename, data):
    with gcs.open(filename, 'w', content_type=upload_file.content_type, options={b'x-goog-acl': b'public-read'}) as gcs_file:
        gcs_file.write(data)















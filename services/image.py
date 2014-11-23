from flask import url_for;


def image_url(image_id, size='thumbnail'):
    return url_for("image.{0}".format(size), object_id=str(image_id))

def image_original_url(image_id, size='original'):
    return url_for("image.{0}".format(size), object_id=str(image_id))


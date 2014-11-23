from flask import Response
from json import dumps
from flask import render_template

def json(data):
    """
    This is the function, which return json data
    """
    return Response(dumps({'data': data}), mimetype='application/json')

def json_template(template_path, **kwargs):
    return Response(render_template(template_path, **kwargs), mimetype='application/json')

template = render_template

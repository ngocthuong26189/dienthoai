from flask import Blueprint
from flask import request, abort, session
from models.chat import Chat
from services import render
from mongoengine import *
from services.paginate import Paginate


module = Blueprint('admin.chat', __name__)

@module.route('/')
def index():
    return render.template('admin/chat/index.html')

@module.route('/manage')
def manage():
    return render.template('admin/chat/manage.html')

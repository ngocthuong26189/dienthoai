from flask import Blueprint
from flask import request, abort, redirect, session, make_response
from services import render, identity
from models.user import User
import json, uuid
module = Blueprint('sites_news', __name__)

@module.route('/')
def index():
    return render.template('sites/news/index.html')
from flask import Blueprint
from flask import request, abort, redirect, session, make_response
from services import render, identity
from models.user import User
from models.news import News
import json
import uuid
module = Blueprint('home', __name__)


@module.route('/')
def index():
    user = {}
    if session.get('user') is not None:
        user = json.loads(session.get("user"))

    return render.template('sites/index.html', user=user)


@module.route('/x-6')
def x6():
    return render.template('sites/x-6.html')


@module.route('/x-8')
def x8():
    return render.template('sites/x-8.html')


@module.route('/x-4')
def x4():
    return render.template('sites/x-4.html')


@module.route('/login', methods=['GET'])
def login():
    return render.template('home/login.html')


@module.route('/login', methods=['POST'])
def do_login():
    data = request.form.to_dict()
    username = data.get('username', None)
    password = data.get('password', None)
    if identity.authenticate(username, password):
        resp = make_response(redirect(request.args.get('next', '/')))
        if json.loads(session['user']).get('permission', 1) > 2:
            userId = json.loads(session.get('user')).get('_id').get('$oid')
            sid = str(uuid.uuid4())
            user = User.objects(id=userId).get()
            user.sid = sid
            user.save()
            user.reload()
            session['user'] = user.to_json()
            resp.set_cookie('userId', userId)
            resp.set_cookie('sid', sid)
        return resp
    else:
        return render.template('home/login.html')


@module.route('/logout')
def logout():
    identity.logout()
    resp = make_response(redirect("/"))
    resp.set_cookie('sid', expires=0)
    resp.set_cookie('userId', expires=0)
    return resp

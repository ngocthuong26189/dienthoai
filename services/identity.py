from functools import wraps
from services import system
from flask import g, request, redirect, url_for, session, abort
from models.user import User, generate_encrypt_password
import json, os

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None and system.get_env() != 'testing':
            return redirect(url_for('home.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def permission_required(code):
    def wrap(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if system.get_env() == 'testing': return f(*args, **kwargs)
            if g.user is None:
                return redirect(url_for('home.login', next=request.url))
            elif json.loads(g.user).get('permission', 1) < code:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return wrap

def authenticate(username, password):
    try:
        user = User.objects.get(username=username)
        encrypt_pwd = generate_encrypt_password(password)
        if encrypt_pwd == user.password:
            if system.get_env() != 'testing': session['user'] = user.to_json()
            return True
        else:
            return False
    except:
        return False

def logout():
    session['user'] = None

def current_user():
    if system.get_env() == 'testing':
        if request.headers.get('REMOTE_USER', None):
            user = User.objects.get(id=request.headers['REMOTE_USER'])
            return user.to_json()
        return 'None'
    return session.get('user', None)

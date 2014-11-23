from flask import Blueprint
from flask import render_template as render
from services import identity


module = Blueprint('home', __name__)


@module.route('/')
def index():
    return render('sites/index.html')

@module.route('/logout')
def logout():
    identity.logout()
    return redirect('/')
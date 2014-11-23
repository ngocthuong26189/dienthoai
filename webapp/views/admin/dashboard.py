from flask import Blueprint
from flask import render_template as render
from services import identity

module = Blueprint('admin.dashboard', __name__)

@module.route('/')
@identity.permission_required(3)
def index():
    return render('admin/dashboard/index.html')

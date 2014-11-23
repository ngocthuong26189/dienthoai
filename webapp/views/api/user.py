from flask import Blueprint
from flask import request
from services import render, identity

module = Blueprint('api.user', __name__)

@module.route('/self', methods=['GET'])
@identity.login_required
def me():
    return identity.current_user()

from flask import Blueprint
from flask import request, abort
from models.order import Order 
from services import render
from mongoengine import *
from services.paginate import Paginate
from services import identity

module = Blueprint('admin.order', __name__)

@module.route('/')
def index():
    data = request.args.to_dict()
    filtering_state = data.get('state__icontains', '')

    criteria = {'state__icontains': str(filtering_state)}
     
    orders = Order.objects(**criteria)
    return render.template('admin/order/index.html', orders=orders)

@module.route('/<int:order_id>', methods=['GET'])
def detail():
    pass

@module.route('<int:order_id>/update', methods=['GET'])
def update(order_id):
    pass

@module.route('/<int:order_id>/delete', methods=['POST'])
def delete(order_id):
    pass


from flask import Blueprint, redirect, url_for
from flask import request, abort
from flask import make_response
from flask import render_template as render
from models.product import Product
from models.order import Order
from services.cart import Cart
from mongoengine import *
import json


module = Blueprint('cart', __name__)

def get_cart_data():
    data = request.cookies.get('cart')
    if data:
        return json.loads(data)
    else:
        return {}

@module.route('/')
def view():
    cart_data = get_cart_data()
    cart = Cart(cart_data)
    return render('sites/cart/view.html', cart=cart)

@module.route('/create')
def create():
    return render('sites/cart/index.html')

@module.route('/add', methods=['POST'])
def add():
    cart_data = get_cart_data()
    cart = Cart(cart_data)

    form_data = request.form.to_dict()
    product_id = str(form_data.get('product_id', None))
    quantity = int(form_data.get('quantity', 1))

    cart.add(product_id, quantity)

    response = make_response(redirect(url_for('cart.view'), code=302))
    response.set_cookie('cart', cart.jsonified_data)
    return response

@module.route('/<string:product_id>/update', methods=['POST'])
def update(product_id):
    cart_data = get_cart_data()
    cart = Cart(cart_data)

    form_data = request.form.to_dict()
    quantity = int(form_data.get('quantity', 1))
    cart.update(product_id, quantity)

    response = make_response(redirect(url_for('cart.view'), code=302))
    response.set_cookie('cart', cart.jsonified_data)
    return response
    
@module.route('/<string:product_id>/delete', methods=['POST'])
def delete(product_id):
    cart_data = get_cart_data()
    cart = Cart(cart_data)

    cart.remove(product_id)

    response = make_response(redirect(url_for('cart.view'), code=302))
    response.set_cookie('cart', cart.jsonified_data)
    return response
    
@module.route('/shipping', methods=['GET'])
def shipping():
    cart_data = get_cart_data()
    cart = Cart(cart_data)
    shipping = cart.shipping_data
    return render('sites/cart/shipping.html', cart=cart, shipping=shipping)

@module.route('/shipping', methods=['POST'])
def update_shipping():
    cart_data = get_cart_data()
    cart = Cart(cart_data)

    form_data = request.form.to_dict()
    # customer_name = form_data.get('customer_name')
    # customer_email = form_data.get('customer_email')
    # customer_phone = form_data.get('customer_phone')
    # customer_address = form_data.get('customer_address')
    # customer_remark = form_data.get('customer_remark')

    cart.update_shipping(form_data)

    response = make_response(redirect(url_for('cart.confirm'), code=302))
    response.set_cookie('cart', cart.jsonified_data)
    return response

@module.route('/confirm', methods=['GET'])
def confirm():
    cart_data = get_cart_data()
    cart = Cart(cart_data)
    return render('sites/cart/confirm.html', cart=cart)

    
@module.route('/checkout', methods=['POST'])
def checkout():
    cart_data = get_cart_data()
    cart = Cart(cart_data)

    data = cart.to_order_data()
    order = Order.objects.create(**data)

    response = make_response(redirect(url_for('cart.thank_you', order_id=order.id), code=302))
    response.set_cookie('cart', '')
    return response

@module.route('/thank_you/<string:order_id>', methods=['GET'])
def thank_you(order_id):
    order = Order.objects.get(id=order_id)
    return render('sites/cart/thank_you.html', order=order)

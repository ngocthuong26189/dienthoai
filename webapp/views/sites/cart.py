from flask import Blueprint, redirect, url_for
from flask import request, abort
from flask import make_response
from flask import render_template as render
from models.product import Product
from services.cart import Cart


module = Blueprint('cart', __name__)

@module.route('/')
def view():
    cart_data = request.cookies.get('cart', '{}')
    cart = Cart(cart_data)
    return render('sites/cart/view.html', cart=cart)


@module.route('/add', methods=['POST'])
def add():
    cart_data = request.cookies.get('cart', '{}')
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
    cart_data = request.cookies.get('cart', '{}')
    cart = Cart(cart_data)

    form_data = request.form.to_dict()
    quantity = int(form_data.get('quantity', 1))
    cart.update(product_id, quantity)

    response = make_response(redirect(url_for('cart.view'), code=302))
    response.set_cookie('cart', cart.jsonified_data)
    return response
    
    
@module.route('/<string:product_id>/delete', methods=['POST'])
def delete(product_id):
    cart_data = request.cookies.get('cart', '{}')
    cart = Cart(cart_data)

    cart.remove(product_id)

    response = make_response(redirect(url_for('cart.view'), code=302))
    response.set_cookie('cart', cart.jsonified_data)
    return response
    
    

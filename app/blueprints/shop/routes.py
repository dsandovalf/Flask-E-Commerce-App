from .import bp as shop
from flask import render_template, redirect, request, flash
from flask_login import login_required, current_user
from app.blueprints.shop.models import Item, Category, Cart


@shop.route('/products', methods=['GET'])#????
@login_required
def products():
    items=Item.query.all()
    return(render_template('products.html.j2',items=items))

@shop.route('/add_to_cart', methods=['GET'])
@login_required
def add_to_cart():
    item_id=request.args.get('id',type=int)
    item=Item.query.filter_by(id=item_id).first()
    item.add_to_cart()
    flash(f'Your {item.name} was added to your cart','warning')
    return redirect(request.referrer)

@shop.route('/mycart',methods=['GET'])
@login_required
def mycart():
    return(render_template('cart.html.j2'))


@shop.route('/remove_item',methods=['GET','POST'])
@login_required
def remove_item():
    item_id=request.args.get('id',type=int)
    Cart.remove_item(item_id)
    item=Item.query.filter_by(id=item_id).first()
    flash(f'You removed {item.name} from your cart', 'success')
    return redirect(request.referrer)

@shop.route('/one_item', methods=['GET'])
@login_required
def one_item():
    item_id=request.args.get('item_id',type=int)
    items=Item.query.filter_by(id=item_id)
    return(render_template('show_items.html.j2',items=items))
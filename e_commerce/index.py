import math


from e_commerce import app, login
from flask import render_template, request, redirect, url_for, session, jsonify
import utils
import cloudinary.uploader
from flask_login import login_user, logout_user, login_required, current_user

from e_commerce.models import UserRole


@app.route('/')
def index():
    cate_id = request.args.get('category_id')
    page = request.args.get('page',1)
    kw = request.args.get('keyword')
    products = utils.read_products(cate_id=cate_id, kw=kw,page=int(page))
    counter = utils.count_products()
    return render_template("index.html",
                            products=products, pages=math.ceil(counter/app.config['PAGE_SIZE']))

@app.route('/register', methods=['get','post'])
def user_register():
    err_msg = ''
    if request.method.__eq__('POST') :
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        confirm = request.form.get('confirm')
        avatar_path = None
        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']
                utils.add_user(name=name, username=username, password=password, email=email, avatar=avatar_path)
                return redirect(url_for('index'))
            else:
                err_msg = 'Mật khẩu không khớp'
        except Exception as ex:
                err_msg = 'Đăng ký thất bại: ' + str(ex)
    return render_template('register.html',err_msg=err_msg)

@app.route('/user-login', methods=['get','post'])
def user_signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = utils.check_login(username, password)
        if(user):
            login_user(user)
            next = request.args.get('next', 'index')
            return redirect(url_for(next))
        else:
            err_msg = 'User hoac Password khong chinh xac'
    return render_template('login.html', err_msg=err_msg)

@app.route('/admin-login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = utils.check_login(username=username, password=password,role=UserRole.ADMIN)
    if (user):
        login_user(user)
    return redirect('/admin')

@app.route('/user-logout')
def user_logout():
    logout_user()
    return redirect(url_for('user_signin'))

@app.context_processor
def common_response():
    return {
        'categories': utils.load_categories(),
        'cart_stats': utils.count_cart(session.get('cart'))
    }

@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id = user_id)

@app.route('/products')
def product_list():
    kw = request.args.get('keyword')
    from_price = request.args.get('from_price')
    to_price = request.args.get('to_price')
    cate_id = request.args.get('category_id')
    products = utils.load_products(cate_id = cate_id, kw = kw, from_price = from_price, to_price = to_price)
    return render_template("products.html",products=products)

@app.route('/cart')
def cart():
    return render_template("cart.html", stats=utils.count_cart(session.get('cart')))

@app.route('/api/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.json
    id = str(data.get('id'))
    name = data.get('name')
    price = data.get('price')
    cart = session.get('cart')
    if not cart:
        cart = {}
    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else:
        cart[id] = {
            'id': id,
            'name': name,
            'price': price,
            'quantity': 1
        }
    session['cart'] = cart
    return jsonify(utils.count_cart(cart))

@app.route("/products/<int:product_id>")
def product_detail(product_id):
    product = utils.get_product_by_id(product_id)
    return render_template('product_detail.html',product=product)

@app.route('/api/pay', methods=['post'])
@login_required
def pay():
    try:
        utils.add_receipt(session.get('cart'))
        del session['cart']
    except:
        return jsonify({'code': 400})

    return jsonify({'code': 200})

if __name__ == '__main__':
    from e_commerce.admin import *
    app.run(debug=True)
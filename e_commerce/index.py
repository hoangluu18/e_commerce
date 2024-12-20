import math

import pytz
from e_commerce import app, login
from flask import render_template, url_for, session, jsonify , redirect
import cloudinary.uploader
from flask_login import login_user, login_required
from e_commerce.models import  Comment
from flask import request
from e_commerce import utils
from flask_login import current_user
from datetime import datetime
from e_commerce import db
from flask_login import logout_user


@app.route("/")
def index():
    kw = request.args.get('kw')
    cate_id = request.args.get('category_id')
    page = request.args.get('page', 1, type=int)

    products = Product.query

    if cate_id:
        products = products.filter(Product.category_id == cate_id)
    if kw:
        products = products.filter(Product.name.contains(kw))

    pagination = products.paginate(page=page, per_page=app.config['PAGE_SIZE'])

    return render_template('index.html',
                           products=pagination.items,
                           pagination=pagination,
                           categories=utils.load_categories(),
                           category_id=cate_id)

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

@app.route('/api/comments', methods=['post'])
@login_required
def add_comment():
    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    current_time = datetime.now(vietnam_tz)
    data = request.json

    comment = Comment(content=data['content'],
                      product_id=data['product_id'],
                      user_id=current_user.id,
                      created_date=current_time)

    db.session.add(comment)
    db.session.commit()

    return jsonify({
        'status': 201,
        'comment': {
            'content': comment.content,
            'created_date': comment.created_date.strftime('%Y-%m-%d %H:%M:%S'),
            'user': {
                'name': current_user.name,
                'avatar': current_user.avatar
            }
        }
    })

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

@app.route('/api/update_cart', methods=['PUT'])
def update_cart():
    data = request.json
    id = str(data.get('id'))
    quantity = data.get('quantity')

    cart = session.get('cart')
    if cart and id in cart:
        cart[id]['quantity'] = quantity
        session['cart'] = cart
    return jsonify(utils.count_cart(cart))

@app.route("/products/<int:product_id>")
def product_detail(product_id):
    product = utils.get_product_by_id(product_id)
    page = int(request.args.get('page', 1))
    comments = utils.get_comments(product_id=product_id, page=page)
    # comments = utils.get_comments(product_id= product_id, page = request.args.get('page', 1))
    return render_template('product_detail.html',
                           comments = comments,
                           product_id = product_id,
                           product = product,
                           pages=math.ceil(utils.count_comments(product_id = product_id)/ app.config['COMMENT_SIZE']))

@app.route("/api/delete-cart/<product_id>", methods=['delete'])
def delete(product_id):
    cart = session.get('cart')
    if cart and product_id in cart:
        del cart[product_id]
        session['cart'] = cart
    return jsonify(utils.count_cart(cart))


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
    from e_commerce.admin import UserRole

    app.run(debug=True)




import math

from e_commerce import app
from flask import render_template, request, redirect, url_for
import utils
import cloudinary.uploader



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

@app.context_processor
def common_response():
    return {
        'categories': utils.load_categories()
    }

@app.route('/products')
def product_list():

    kw = request.args.get('keyword')
    from_price = request.args.get('from_price')
    to_price = request.args.get('to_price')

    cate_id = request.args.get('category_id')
    products = utils.load_products(cate_id = cate_id, kw = kw, from_price = from_price, to_price = to_price)
    return render_template("products.html",products=products)

@app.route("/products/<int:product_id>")
def product_detail(product_id):
    product = utils.get_product_by_id(product_id)
    return render_template('product_detail.html',product=product)

if __name__ == '__main__':
    from e_commerce.admin import *
    app.run(debug=True)
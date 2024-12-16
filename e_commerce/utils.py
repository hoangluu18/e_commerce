import json
from zoneinfo import available_timezones

from flask_login import current_user
from sqlalchemy.testing.suite.test_reflection import users

from e_commerce import app, db
from e_commerce.models import Category, Product, User, Receipt, ReceiptDetail, UserRole, Comment
from sqlalchemy import func, extract
import hashlib

def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def load_categories():
    return Category.query.all()

def read_products(cate_id=None, kw=None, from_price=None, to_price=None, page=1):
    # Lọc sản phẩm chỉ khi active = True
    products = Product.query.filter(Product.active.is_(True))

    # Lọc theo cate_id nếu có
    if cate_id:
        products = products.filter(Product.category_id == cate_id)

    # Lọc theo từ khóa nếu có
    if kw:
        products = products.filter(Product.name.contains(kw))

    # Lọc theo khoảng giá nếu có
    if from_price is not None:
        products = products.filter(Product.price >= from_price)
    if to_price is not None:
        products = products.filter(Product.price <= to_price)

    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size

    return products.slice(start, end).all()


def count_products():
    return Product.query.filter(Product.active.is_(True)).count()
def get_product_by_id(product_id):
    return Product.query.get(product_id)

def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                email=kwargs.get('email'),
                avatar = kwargs.get('avatar'))
    db.session.add(user)
    db.session.commit()


def check_login(username, password, role=UserRole.USER):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return User.query.filter(User.username.__eq__(username.strip()), User.password.__eq__(password), User.user_role.__eq__(role)).first()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def count_cart(cart):
    total_quantity, total_amount = 0, 0
    if cart:
        for c in cart.values():
            quantity = int(c['quantity'])  # Chuyển quantity về kiểu int
            price = float(c['price'])  # Chuyển price về kiểu float
            total_quantity += quantity
            total_amount += quantity * price
    return {
        'total_quantity': total_quantity,
        'total_amount': total_amount
    }
def add_receipt(cart):
    if cart:
        receipt = Receipt(user=current_user)
        db.session.add(receipt)

        for c in cart.values():
            d = ReceiptDetail(receipt=receipt, product_id=c['id'],quantity=c['quantity'], unit_price=c['price'])
            db.session.add(d)

        db.session.commit()


def category_stats():
    return db.session.query(Category.id, Category.name, func.count(Product.id))\
        .join(Product, Category.id.__eq__(Product.category_id), isouter=True).group_by(Category.id, Category.name).all()

def product_stats(kw = None, from_date = None, to_date = None):
    p = db.session.query(Product.id, Product.name, func.sum(ReceiptDetail.quantity * ReceiptDetail.unit_price))\
            .join(ReceiptDetail, ReceiptDetail.product_id.__eq__(Product.id), isouter=True)\
            .join(Receipt, Receipt.id.__eq__(ReceiptDetail.receipt_id))\
            .group_by(Product.id, Product.name)
    if kw:
       p = p.filter(Product.name.contains(kw))
    if from_date:
        p = p.filter(Receipt.created_date.__ge__(from_date))
    if to_date:
        p = p.filter(Receipt.created_date.__le__(to_date))
    return p.all()

def product_month_stats(year):
    return db.session.query(extract('month',Receipt.created_date), func.sum(ReceiptDetail.quantity * ReceiptDetail.unit_price))\
        .join(ReceiptDetail, ReceiptDetail.receipt_id.__eq__(Receipt.id))\
        .filter(extract('year', Receipt.created_date) == year)\
        .group_by(extract('month', Receipt.created_date))\
        .order_by(extract('month', Receipt.created_date)).all()

def add_comment(content, product_id):
    c = Comment(content=content, product_id=product_id, user=current_user)
    db.session.add(c)
    db.session.commit()
    return c


def get_comments(product_id, page = 1):
    page_size = app.config['COMMENT_SIZE']
    start = (page - 1) * page_size
    return Comment.query.filter(Comment.product_id.__eq__(product_id))\
            .order_by(-Comment.id).slice(start, start + page_size).all()

def count_comments(product_id):
    return Comment.query.filter(Comment.product_id.__eq__(product_id)).count()
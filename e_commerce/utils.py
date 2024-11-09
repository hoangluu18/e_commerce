import json
from zoneinfo import available_timezones

from e_commerce import app, db
from e_commerce.models import Category, Product, User
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

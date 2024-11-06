import json

from e_commerce import app
from e_commerce.models import Category, Product

def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def load_categories():
    return Category.query.all()

def load_products(cate_id=None, kw=None, from_price=None, to_price=None):
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

    return products.all()

def get_product_by_id(product_id):
    return Product.query.get(product_id)
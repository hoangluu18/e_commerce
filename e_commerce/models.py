from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Float, Enum
from datetime import datetime
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from e_commerce import db
from e_commerce import app
from enum import Enum as UserEnum


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

class UserRole(UserEnum):
    ADMIN = 1
    USER = 2

class User(BaseModel, UserMixin):
    name = Column(String(50), nullable= False)
    username = Column(String(50), nullable= False, unique=True)
    password = Column(String(50), nullable= False)
    avatar = Column(String(100))
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Category(BaseModel):
    __tablename__ = 'category'
    name = Column(String(20), nullable=False)
    products = relationship('Product', backref='category', lazy=False)
    def __str__(self):
        return self.name



class Product(BaseModel):
    __tablename__ = 'product'
    name = Column(String(50), nullable=False)
    description = Column(String(500))
    price = Column(Float, default=0)
    image = Column(String(500))
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)

    # Technical specifications
    screen = Column(String(100))
    os = Column(String(50))
    rear_camera = Column(String(100))
    front_camera = Column(String(50))
    cpu = Column(String(100))
    ram = Column(String(20))
    internal_memory = Column(String(20))
    battery = Column(String(50))

    receipt_details = relationship("ReceiptDetail", backref="product", lazy=True)
    comments = relationship("Comment", backref="product", lazy=True)

    def __str__(self):
        return self.name
class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetail', backref='receipt', lazy=True)

class ReceiptDetail(db.Model):
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False, primary_key=True)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False, primary_key=True)
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0)

class Comment(BaseModel):
    content = Column(String(255), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    def __str__(self):
        return self.content


if __name__ == '__main__':
    with app.app_context():


        db.create_all()


        # products = [{
        # "id": 1,
        # "name": "iPhone 7 Plus",
        # "description": "Apple, 32GB, RAM: 3GB, iOS13",
        # "price": 17000000,
        # "image": "images/p1.png",
        # "category_id": 1
        # }, {
        # "id": 2,
        # "name": "iPad Pro 2020",
        # "description": "Apple, 128GB, RAM: 6GB",
        # "price": 37000000,
        #     "image": "images/p2.png",
        # "category_id": 2
        # }, {
        # "id": 3,
        # "name": "Galaxy Note 10 Plus",
        # "description": "Samsung, 64GB, RAML: 6GB",
        # "price": 24000000,
        # "image": "images/p3.png",
        # "category_id": 1
        # }]
        # for p in products:
        #     pro = Product(name = p['name'], price = p['price'], image = p['image'],description = p['description'] , category_id = p['category_id'])
        #     db.session.add(pro)
        #
        # db.session.commit()
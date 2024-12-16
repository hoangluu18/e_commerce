import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import cloudinary
from flask_login import LoginManager

load_dotenv()

app = Flask(__name__)

app.secret_key='@#%#%$$$^%$^%$%#%^%^&&*&^*^&%^&%&%^%'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://luuhoang:Pmshoanghot1%40@luuhoang.mysql.pythonanywhere-services.com/luuhoang$saleappdb?charset=utf8mb4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://luuhoang:Pmshoanghot1%40@luuhoang.mysql.pythonanywhere-services.com/luuhoang$saleappdb?charset=utf8mb4'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 4
db = SQLAlchemy(app=app)



cloudinary.config(
    cloud_name='daku3kfyd',
    api_key='572181413815548',
    api_secret='b5RbspGDne2wIasbPK268IMfkGY',
    api_proxy = "http://proxy.server:3128",
    secure=True

)

login = LoginManager(app = app)
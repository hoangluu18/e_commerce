import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import cloudinary
from flask_login import LoginManager

load_dotenv()

app = Flask(__name__)

app.secret_key='@#%#%$$$^%$^%$%#%^%^&&*&^*^&%^&%&%^%'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 4
db = SQLAlchemy(app=app)



cloudinary.config(
    cloud_name=os.getenv('CLOUD_NAME'),
    api_key=os.getenv('API_KEY'),
    api_secret=os.getenv('API_SECRET')
)

login = LoginManager(app = app)
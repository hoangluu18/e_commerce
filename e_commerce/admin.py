from datetime import datetime
from urllib import request

from e_commerce import app, db
from e_commerce.models import Category, Product, UserRole
from flask_admin import Admin, expose, AdminIndexView
from flask_admin import BaseView
from flask_admin.contrib.sqla import ModelView
from wtforms import SelectField
from flask_login import current_user, logout_user
import utils
from flask import redirect
from flask import request
from flask import current_app

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

from wtforms.fields import SelectField
from flask_admin.contrib.sqla import ModelView
from e_commerce.models import Category


class ProductView(ModelView):
    can_view_details = True
    can_export = True
    column_filters = ['name', 'price']
    column_searchable_list = ('name', 'description')
    column_list = ('name', 'description', 'price', 'image', 'active', 'created_date', 'category','screen','ram','cpu','internal_memory','os','rear_camera','front_camera','battery')

    def scaffold_form(self):
        form = super(ProductView, self).scaffold_form()

        # Thiết lập SelectField với choices từ Category sử dụng lambda
        form.category_id = SelectField(
            'Category',
            choices=lambda: [(category.id, category.name) for category in Category.query.all()],
            coerce=int
        )

        return form

        return form
class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated

class StatsView(BaseView):
    @expose('/')
    def __index__(self):
        kw = request.args.get('kw')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        year = request.args.get('year',datetime.now().year)

        return self.render('admin/stats.html',
                           month_stats = utils.product_month_stats(year = year),
                           stats = utils.product_stats(kw = kw, from_date = from_date, to_date = to_date))
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', stats = utils.category_stats())

admin = Admin(app=app, name='E-commerce Administration', template_mode='bootstrap4', index_view=MyAdminIndexView())
admin.add_view(AuthenticatedModelView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(LogoutView(name='Logout', endpoint='/logout'))
admin.add_view(StatsView(name='Stats', endpoint='/stats'))
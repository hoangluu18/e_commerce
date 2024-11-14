from e_commerce import app, db
from e_commerce.models import Category, Product, UserRole
from flask_admin import Admin, expose
from flask_admin import BaseView
from flask_admin.contrib.sqla import ModelView
from wtforms import SelectField
from flask_login import current_user, logout_user
from flask import redirect
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
    column_list = ('name', 'description', 'price', 'image', 'active', 'created_date', 'category')

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

admin = Admin(app=app, name='E-commerce Administration', template_mode='bootstrap4')
admin.add_view(AuthenticatedModelView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(LogoutView(name='Logout', endpoint='/logout'))
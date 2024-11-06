from random import choices

from e_commerce import app, db
from e_commerce.models import Category, Product
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from wtforms import SelectField


class ProductView(ModelView):
    can_view_details = True
    column_list = ('name','description', 'price', 'Image', 'active', 'created_date', 'category')

    def scaffold_form(self):
        def get_choices(product_id=None):
            if product_id:
                return [(category.id, category.name) for category in Category.query.filter_by(id=product_id).all()]
            return [(category.id, category.name) for category in Category.query.all()]
        form = super(ProductView, self).scaffold_form()

        # Lấy các lựa chọn cho category_id từ cơ sở dữ liệu
        with app.app_context():
            choices = get_choices()

        # Kiểm tra và thiết lập category_id nếu không có trong form
        form.category_id = SelectField('Category', choices=choices, coerce=int)

        # Lấy các lựa chọn cho category_id từ cơ sở dữ liệu
        with app.app_context():
            form.category_id.choices = [(category.id, category.name) for category in Category.query.all()]

        return form


admin = Admin(app=app, name='E-commerce Administration', template_mode='bootstrap4')
admin.add_view(ModelView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
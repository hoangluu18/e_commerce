from e_commerce import app, db
from e_commerce.models import Category, Product
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
class ProductView(ModelView):
    can_view_details = True
    # with app.app_context():
    #     form_args = {
    #         'category_id': {
    #             'choices': [(category.id, category.name) for category in Category.query.all()]
    #         }
    #     }

admin = Admin(app=app, name='E-commerce Administration', template_mode='bootstrap4')
admin.add_view(ModelView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
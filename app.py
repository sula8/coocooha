from flask import Flask
from flask import redirect, url_for, request

from flask_migrate import Migrate
from flask_security import Security
from flask_security import current_user

from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from models import db, User, Recipe, Ingredient, IngredientGroup, Role
from config import Config

from main.main import main
from recipe.recipe import recipe
from wizard.wizard import wizard
from favorites.favorites import favorites
from registration.registration import user_creation, user_datastore


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

migrate = Migrate(app, db)

security = Security(app, user_datastore)


class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


admin = Admin(app, 'FlaskApp', url='/', index_view=HomeAdminView(name='Home'))


admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Recipe, db.session))
admin.add_view(AdminView(Ingredient, db.session))
admin.add_view(AdminView(IngredientGroup, db.session))
admin.add_view(AdminView(Role, db.session))


app.register_blueprint(main, url_prefix='/')
app.register_blueprint(recipe, url_prefix='/recipe')
app.register_blueprint(wizard, url_prefix='/wizard')
app.register_blueprint(favorites, url_prefix='/favorites')
app.register_blueprint(user_creation, url_prefix='/registration')

import errorhandlers

#TODO: сделать фабрику приложения

#TODO: удалить это: export DATABASE_URL='postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/coocooha'
#TODO: удалить это: export FLASK_ENV=development


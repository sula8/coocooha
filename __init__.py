import os

from flask import Flask
from flask_migrate import Migrate
from flask_security import Security
from flask_admin import Admin

from main.main import main
from recipe.recipe import recipe
from wizard.wizard import wizard
from favorites.favorites import favorites
from registration.registration import user_creation, user_datastore

from administrator import AdminView, HomeAdminView

from models import db, User, Recipe, Ingredient, IngredientGroup, Role

from errorhandlers import page_not_found, method_not_allowed

app_dir = os.path.abspath(os.path.dirname(__file__))


def create_app(config):

	app = Flask(__name__)

	app.config.from_object(config)

	db.init_app(app)

	migrate = Migrate(app, db)

	security = Security(app, user_datastore)

	#Flask-Admin
	admin = Admin(app, 'FlaskApp', url='/', index_view=HomeAdminView(name='Home'))

	admin.add_view(AdminView(User, db.session))
	admin.add_view(AdminView(Recipe, db.session))
	admin.add_view(AdminView(Ingredient, db.session))
	admin.add_view(AdminView(IngredientGroup, db.session))
	admin.add_view(AdminView(Role, db.session))


	#Blueprints
	app.register_blueprint(main, url_prefix='/')
	app.register_blueprint(recipe, url_prefix='/recipe')
	app.register_blueprint(wizard, url_prefix='/wizard')
	app.register_blueprint(favorites, url_prefix='/favorites')
	app.register_blueprint(user_creation, url_prefix='/registration')


	#Errorhandlers
	app.register_error_handler(404, page_not_found)
	app.register_error_handler(405, method_not_allowed)

	return app



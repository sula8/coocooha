from flask import Flask
from flask import redirect

from flask_migrate import Migrate
from flask_security import Security

from flask_admin import Admin
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

admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Recipe, db.session))
admin.add_view(ModelView(Ingredient, db.session))
admin.add_view(ModelView(IngredientGroup, db.session))
admin.add_view(ModelView(Role, db.session))


app.register_blueprint(main, url_prefix='/')
app.register_blueprint(recipe, url_prefix='/recipe')
app.register_blueprint(wizard, url_prefix='/wizard')
app.register_blueprint(favorites, url_prefix='/favorites')
app.register_blueprint(user_creation, url_prefix='/registration')


@app.errorhandler(404)
def page_not_found(e):
    return '404 error', 404


@app.errorhandler(405)
def page_not_found(e):
    return redirect('/'), 405


#export DATABASE_URL='postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/coocooha'
#export FLASK_ENV=development

#TODO:секьюр админ и регистрация(пароль)
#TODO:картинки
#TODO:эррор хэндлеры
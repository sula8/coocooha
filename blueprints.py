from app import app

from recipe.recipe import recipe
from wizard.wizard import wizard
from favorites.favorites import favorites
from registration.registration import user_creation
from main.main import main


app.register_blueprint(main, url_prefix='/')
app.register_blueprint(recipe, url_prefix='/recipe')
app.register_blueprint(wizard, url_prefix='/wizard')
app.register_blueprint(favorites, url_prefix='/favorites')
app.register_blueprint(user_creation, url_prefix='/registration')

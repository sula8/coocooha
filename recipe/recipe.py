from flask import Blueprint
from flask import session
from flask import render_template

from models import Recipe, User


recipe = Blueprint('recipes', __name__, template_folder='templates')


@recipe.route('/<recipe_id>/')
def render_recipe(recipe_id):
    recipe_in_fav = False
    wizard_results = False
    user_ingredients = None

    curr_recipe = Recipe.query.filter(Recipe.id == recipe_id).first()

    if session.get('user_id'):
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()

        if curr_recipe in user.favorites:
            recipe_in_fav = True

    if session.get('user_ingredients'):
        user_ingredients = session.get('user_ingredients')

    if session.get('wizard_results'):
        wizard_results = True

    return render_template('recipe/recipe.html',
                           recipe=curr_recipe,
                           recipe_in_fav=recipe_in_fav,
                           user_ingredients=user_ingredients,
                           wizard_results=wizard_results)

from os import path

from flask import Blueprint
from flask import send_file
from flask import session
from flask import render_template
from flask_login import current_user

from ..models import Recipe

PIC_FOLDER = 'pictures'

recipe = Blueprint('recipes', __name__, template_folder='templates')


@recipe.route('/<recipe_id>/')
def render_recipe(recipe_id):
    recipe_in_fav = False
    wizard_results = False
    user_ingredients = None

    curr_recipe = Recipe.query.filter(Recipe.id == recipe_id).first()

    if current_user.is_authenticated and (curr_recipe in current_user.favorites):
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


@recipe.route('/pictures/<path:filename>')
def get_recipe_pic(filename):
    print(path.join('recipe', 'pictures', filename))
    return send_file(path.join('recipe', 'pictures', filename))

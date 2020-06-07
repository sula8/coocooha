from flask import Blueprint
from flask import session
from flask import request
from flask import render_template

from ..models import Recipe, Ingredient, IngredientGroup

wizard = Blueprint('wizard', __name__, template_folder='templates')


@wizard.route('/')
def render_wizard():
    ing_gr = IngredientGroup.query.all()
    ing = Ingredient()

    if session.get('wizard_results'):
        session.pop('wizard_results')

    return render_template("wizard/list.html", ing_gr=ing_gr, ing=ing)


@wizard.route('/results/', methods=["GET", "POST"])
def render_wizard_results():

    if session.get('wizard_results'):
        recipes_ids = session.get('wizard_results')
        recipes = Recipe.query.filter(Recipe.id.in_(recipes_ids)).all()
        return render_template('wizard/recipes.html', recipes=recipes)

    ings = request.form
    user_ingredients = [int(ing_id) for ing_id in ings.values()]
    session['user_ingredients'] = user_ingredients

    ingredients = Ingredient.query.filter(Ingredient.id.in_(user_ingredients)).all()

    recipes = get_recipes(ingredients, user_ingredients)

    session['wizard_results'] = [r.id for r in recipes]

    return render_template('wizard/recipes.html', recipes=recipes)


def get_recipes(ingredients, user_ingredients):
    recipes = []
    for ing in ingredients:
        recipes_query = Recipe.query.filter(Recipe.ingredients.contains(ing))
        for recipe in recipes_query:
            if recipe not in recipes:
                recipes.append(recipe)

    for recipe in recipes:
        recipe_ingredients = [r.id for r in recipe.ingredients]
        counter = 0
        for ing in user_ingredients:
            if ing in recipe_ingredients:
                counter += 1
        recipe.counter = counter

    recipes_sorted = sorted(recipes, key=lambda r: r.counter, reverse=True)

    return recipes_sorted


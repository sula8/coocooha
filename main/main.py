from flask import Blueprint
from flask import render_template
from sqlalchemy import func

from models import Recipe, recipe_user_assn


main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def render_main():
    total_favs = func.count(recipe_user_assn.c.user_id)
    recipes = Recipe.query.join(recipe_user_assn).group_by(Recipe).order_by(total_favs.desc()).limit(6).all()
    return render_template("main/index.html", recipes=recipes)

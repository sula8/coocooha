from flask import Blueprint
from flask import url_for
from flask import request
from flask import redirect
from flask import session
from flask import render_template

from models import db, Recipe, User

favorites = Blueprint('favorites', __name__, template_folder='templates')


@favorites.route('/')
def render_favs():
    if not session.get("user_id"):
        return redirect("/login")
    user_id = session.get("user_id")

    user = User.query.filter(User.id == user_id).first()
    msg = request.args.get('msg')

    return render_template("favorites/fav.html", favs=user.favorites, msg=msg)


@favorites.route('/add/<int:recipe_id>/', methods=["POST"])
def add_to_fav(recipe_id):
    if not session.get("user_id"):
        return redirect("/login")

    user_id = session.get("user_id")
    user = User.query.filter(User.id == user_id).first()
    recipe = Recipe.query.filter(Recipe.id == recipe_id).first()

    if recipe not in user.favorites:
        user.favorites.append(recipe)
        db.session.add(user)
        db.session.commit()
        msg = "Блюдо добавлено в избранное."

    return redirect(url_for('render_favs', msg=msg))


@favorites.route('/remove/<int:recipe_id>/', methods=["POST"])
def remove_fav(recipe_id):
    if not session.get("user_id"):
        return redirect("/login")

    user_id = session.get("user_id")
    user = User.query.filter(User.id == user_id).first()
    recipe = Recipe.query.filter(Recipe.id == recipe_id).first()

    if recipe in user.favorites:
        user.favorites.remove(recipe)
        db.session.commit()
        msg = "Блюдо удалено из избранного."

    return redirect(url_for('render_favs', msg=msg))


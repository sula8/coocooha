from flask import Blueprint
from flask import url_for
from flask import request
from flask import redirect
from flask import render_template

from flask_login import current_user
from flask_security import login_required

from models import db, Recipe

favorites = Blueprint('favorites', __name__, template_folder='templates')


@favorites.route('/')
@login_required
def render_favs():
    user = current_user
    msg = request.args.get('msg')
    return render_template("favorites/fav.html", favs=user.favorites, msg=msg)


@favorites.route('/add/<int:recipe_id>/', methods=["POST"])
@login_required
def add_to_fav(recipe_id):
    user = current_user

    recipe = Recipe.query.filter(Recipe.id == recipe_id).first()

    if recipe not in user.favorites:
        user.favorites.append(recipe)
        db.session.add(user)
        db.session.commit()
        msg = "Блюдо добавлено в избранное."
    else:
        msg = "Блюдо уже было добавлено в избранное."

    return redirect(url_for('favorites.render_favs', msg=msg))


@favorites.route('/remove/<int:recipe_id>/', methods=["POST"])
@login_required
def remove_fav(recipe_id):
    user = current_user
    recipe = Recipe.query.filter(Recipe.id == recipe_id).first()

    if recipe in user.favorites:
        user.favorites.remove(recipe)
        db.session.commit()
        msg = "Блюдо удалено из избранного."
    else:
        msg = "Этого блюда не было избранном."

    return redirect(url_for('favorites.render_favs', msg=msg))


from flask import Flask
from flask import url_for
from flask import render_template
from flask import session
from flask import redirect
from flask import request

from flask_migrate import Migrate
from sqlalchemy import func

from models import db, Recipe, User, IngredientGroup, Ingredient, recipe_user_assn
from forms import RegistrationForm, LoginForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

migrate = Migrate(app, db)


@app.route('/')
def index():
    total_favs = func.count(recipe_user_assn.c.user_id)
    recipes = Recipe.query.join(recipe_user_assn).group_by(Recipe).order_by(total_favs.desc()).limit(6).all()

    return render_template("index.html", recipes=recipes)


@app.route('/recipe/<recipe_id>/')
def render_recipe(recipe_id):
    recipe_in_fav = False
    wizard_results = False
    user_ingredients = None

    recipe = Recipe.query.filter(Recipe.id == recipe_id).first()

    if session.get('user_id'):
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()

        if recipe in user.favorites:
            recipe_in_fav = True

    if session.get('user_ingredients'):
        user_ingredients = session.get('user_ingredients')

    if session.get('wizard_results'):
        wizard_results = True

    return render_template('recipe.html',
                           recipe=recipe,
                           recipe_in_fav=recipe_in_fav,
                           user_ingredients=user_ingredients,
                           wizard_results=wizard_results)


@app.route("/registration/", methods=["GET", "POST"])
def registration():
    if session.get("user_id"):
        return redirect("/")

    form = RegistrationForm()

    if request.method == "POST":
        user = User.query.filter(User.email == form.email.data).first()
        if user:
            msg = "Пользователь уже существует"
            return render_template("registration.html", form=form, msg=msg)

        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        return render_template("registration_success.html", form=form, email=user.email)

    return render_template("registration.html", form=form)


@app.route("/login/", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect("/")

    # Создаем форму
    form = LoginForm()

    if request.method == "POST":

        # Если форма не валидна
        if not form.validate_on_submit():

            # показываем форму и не забываем передать форму в шаблон
            return render_template("login.html", form=form)

        #Информацию о пользователе берем из базы по введенной почте
        user = User.query.filter(User.email == form.email.data).first()

        # Данные берем из формы
        if not user or user.password != form.password.data:

            # Добавляем ошибку для поля формы
            form.email.errors.append("Неверное имя или пароль")

        else:
            session["user_id"] = user.id
            return redirect("/")

    return render_template("login.html", form=form)


@app.route('/logout/', methods=["POST"])
def logout():
    if session.get("user_id"):
        session.pop("user_id")
    return redirect("/login")


@app.route('/add_fav/<int:recipe_id>/', methods=["POST"])
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


@app.route('/remove_fav/<int:recipe_id>/', methods=["POST"])
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


@app.route('/favorites/')
def render_favs():
    if not session.get("user_id"):
        return redirect("/login")
    user_id = session.get("user_id")

    user = User.query.filter(User.id == user_id).first()
    msg = request.args.get('msg')

    return render_template("fav.html", favs=user.favorites, msg=msg)


@app.route('/wizard/')
def render_wizard():
    ing_gr = IngredientGroup.query.all()
    ing = Ingredient()
    return render_template("list.html", ing_gr=ing_gr, ing=ing)


@app.route('/wizard-results/', methods=["GET", "POST"])
def render_wizard_results():

    if session.get('wizard_results'):
        recipes_ids = session.get('wizard_results')
        recipes = Recipe.query.filter(Recipe.id.in_(recipes_ids)).all()
        return render_template("recipes.html", recipes=recipes)

    ing = request.form
    user_ingredients = [int(ing_id) for ing_id in ing.values()]
    session['user_ingredients'] = user_ingredients

    ingredients = Ingredient.query.filter(Ingredient.id.in_(user_ingredients)).all()

    recipes = get_recipes(ingredients, user_ingredients)

    session['wizard_results'] = [r.id for r in recipes]

    return render_template("recipes.html", recipes=recipes)


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


@app.errorhandler(404)
def page_not_found(e):
    return '404 error', 404


@app.errorhandler(405)
def page_not_found(e):
    return redirect('/'), 405

#export DATABASE_URL='postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/coocooha'

#TODO:блупринты

#TODO: логин
#TODO: шапка - передать user


#TODO:урл_фор
#TODO:картинки
#TODO:эррор хэндлер
#TODO:контекст
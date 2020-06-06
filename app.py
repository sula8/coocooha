from flask import Flask
from flask import render_template
from flask import session
from flask import redirect
from flask import request

from flask_migrate import Migrate

from flask_security import Security
#from flask_security import SQLAlchemyUserDatastore

from models import db, User, Role
from forms import LoginForm
from config import Config

from recipe.recipe import recipe
from wizard.wizard import wizard
from favorites.favorites import favorites
from registration.registration import user_creation, user_datastore
from main.main import main


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(main, url_prefix='/')
app.register_blueprint(recipe, url_prefix='/recipe')
app.register_blueprint(wizard, url_prefix='/wizard')
app.register_blueprint(favorites, url_prefix='/favorites')
app.register_blueprint(user_creation, url_prefix='/registration')


#user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


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


#export DATABASE_URL='postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/coocooha'

#TODO:блупринты

#TODO: логин
#TODO: шапка - передать user


#TODO:урл_фор
#TODO:картинки
#TODO:эррор хэндлеры
#TODO:контекст

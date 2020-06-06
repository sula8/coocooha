from flask import Blueprint
from flask import request
from flask import redirect
from flask import session
from flask import render_template

from flask_security import SQLAlchemyUserDatastore

from app import db
from forms import RegistrationForm
from models import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

user_creation = Blueprint('registration', __name__, template_folder='templates')


@user_creation.route("/", methods=["GET", "POST"])
def registration():
    if session.get("user_id"):
        return redirect("/")

    form = RegistrationForm()

    if request.method == "POST":
        user = User.query.filter(User.email == form.email.data).first()
        if user:
            msg = "Пользователь уже существует"
            return render_template("registration.html", form=form, msg=msg)

        user = user_datastore.create_user(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        return render_template("registration/registration_success.html", form=form, email=user.email)

    return render_template("registration/registration.html", form=form)

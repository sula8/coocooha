from flask import Blueprint
from flask import request
from flask import redirect
from flask import session
from flask import render_template

from flask_security import SQLAlchemyUserDatastore
from flask_security.utils import hash_password

from models import db
from forms import RegistrationForm
from models import User, Role


user_creation = Blueprint('registration', __name__, template_folder='templates')


user_datastore = SQLAlchemyUserDatastore(db, User, Role)


@user_creation.route("/", methods=["GET", "POST"])
def registration():
    if session.get("user_id"):
        return redirect("/")

    form = RegistrationForm()

    if request.method == "POST":
        user = User.query.filter(User.email == form.email.data).first()
        if user:
            msg = "Пользователь уже существует"
            return render_template("registration/registration.html", form=form, msg=msg)

        user = user_datastore.create_user(email=form.email.data, password=hash_password(form.password.data))
        role = Role.query.filter(Role.name == 'user').first()
        db.session.add(user)
        user_datastore.add_role_to_user(user, role)
        db.session.commit()

        return render_template("registration/registration_success.html", form=form, email=user.email)

    return render_template("registration/registration.html", form=form)

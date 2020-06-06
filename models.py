from flask_sqlalchemy import SQLAlchemy

from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()


recipe_ingredient_assn = db.Table('recipe_ingredient',
	db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id')),
	db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredients.id')),
)


recipe_user_assn = db.Table('recipe_user',
	db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id')),
	db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
)


roles_users = db.Table('roles_users',
	db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
	db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
)


class Recipe(db.Model):
	__tablename__ = 'recipes'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String)
	picture = db.Column(db.String)
	description = db.Column(db.String)
	time = db.Column(db.Integer)
	servings = db.Column(db.Integer)
	kcal = db.Column(db.Integer)
	instruction = db.Column(db.Text)

	ingredients = db.relationship('Ingredient', secondary=recipe_ingredient_assn, back_populates='recipes')
	users = db.relationship('User', secondary=recipe_user_assn, back_populates='favorites')


class Ingredient(db.Model):
	__tablename__ = 'ingredients'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String)
	ingredient_group_id = db.Column(db.Integer, db.ForeignKey('ingredient_groups.id'))

	recipes = db.relationship('Recipe', secondary=recipe_ingredient_assn, back_populates='ingredients')
	ingredient_groups = db.relationship('IngredientGroup', back_populates='ingredients')


class IngredientGroup(db.Model):
	__tablename__ = 'ingredient_groups'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String)

	ingredients = db.relationship('Ingredient', back_populates='ingredient_groups')


class User(db.Model, UserMixin):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.String, unique=True)
	password = db.Column(db.String)
	active = db.Column(db.Boolean())

	roles = db.relationship('Role', secondary=roles_users, backref=db.backref('user', lazy='dynamic'))
	favorites = db.relationship('Recipe', secondary=recipe_user_assn, back_populates='users')


class Role(db.Model, RoleMixin):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(100), unique=True)
	description = db.Column(db.String(255))

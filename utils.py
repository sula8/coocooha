import json
from models import db, IngredientGroup, Ingredient, Recipe
from app import app


def groups_to_bd():
	with open("ingredient_groups.json", "r") as f:
		ingredient_groups = json.load(f)

	for group in ingredient_groups:
		ig_group = IngredientGroup(
			id=group['id'],
			title=group['title']
		)
		db.session.add(ig_group)

	db.session.commit()


def igs_to_bd():
	with open("ingredients.json", "r") as f:
		ingredients = json.load(f)

	for ingredient in ingredients:
		ig = Ingredient(
			id=ingredient['id'],
			title=ingredient['title'],
			ingredient_group_id=ingredient['ingredient_group']
		)
		db.session.add(ig)

	db.session.commit()


def recipe_to_bd():
	with open("recipes.json", "r") as f:
		recipes = json.load(f)

	for recipe in recipes:
		recipe_db = Recipe(
			id=recipe['id'],
			title=recipe['title'],
			picture=recipe['picture'],
			description=recipe['description'],
			time=recipe['time'],
			kcal=recipe['kcal'],
			instruction=recipe['instruction'],
			servings=recipe['servings']
		)

		db.session.add(recipe_db)

		for ig in recipe['ingredients']:
			ig_id_db = Ingredient.query.filter(Ingredient.id == ig).first()
			recipe_db.ingredients.append(ig_id_db)

		db.session.add(recipe_db)

	db.session.commit()


def fix_recipe(): # функция для того чтобы что-то конкретное изменить в рецептах в бд
	with open("recipes.json", "r") as f:
		recipes = json.load(f)

	for recipe in recipes:
		recipe_db = Recipe.query.filter(Recipe.id == recipe['id']).first()
		recipe_db.picture = f"item{recipe['id']}.jpg"

		db.session.add(recipe_db)

	db.session.commit()


with app.app_context():
	db.init_app(app)
	fix_recipe()

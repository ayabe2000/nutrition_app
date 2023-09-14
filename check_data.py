from app import db, app
from models import Food


with app.app_context():
    foods = Food.query.all()
    for food in foods:
        print(f"Name: {food.name}, Energy: {food.energy_kcal_100g}kcal, Protein: {food.protein_per_100g}g, Fat: {food.fat_per_100g}g, Cholesterol: {food.cholesterol_per_100g}mg, Carbohydrates: {food.carbs_per_100g}g")

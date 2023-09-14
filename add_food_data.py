from app import db,app
from models import Food
from datetime import datetime


try:
    with app.app_context():
        print("Starting to add food data...")

        # 食品データをリストに追加
        food_data = [
            {"name": "こむぎ", "energy_kcal_100g": 337, "protein_per_100g": 10.6, "fat_per_100g": 3.1, "cholesterol_per_100g": 1, "carbs_per_100g": 72.2},
            {"name": "食パン", "energy_kcal_100g": 264, "protein_per_100g": 9.3, "fat_per_100g": 4.4, "cholesterol_per_100g": 1, "carbs_per_100g": 46.7},
            {"name": "うどん", "energy_kcal_100g": 270, "protein_per_100g": 6.1, "fat_per_100g": 0.6, "cholesterol_per_100g": 1, "carbs_per_100g": 56.8},
            {"name": "こめ", "energy_kcal_100g": 353, "protein_per_100g": 6.8, "fat_per_100g": 2.7, "cholesterol_per_100g": 1, "carbs_per_100g": 74.3},
            {"name": "いも", "energy_kcal_100g": 35, "protein_per_100g": 1.9, "fat_per_100g": 0.4, "cholesterol_per_100g": 1, "carbs_per_100g": 14.7},
            {"name": "あずき", "energy_kcal_100g": 339, "protein_per_100g": 20.3, "fat_per_100g": 2.2, "cholesterol_per_100g": 1, "carbs_per_100g": 58.7},
            {"name": "オクラ", "energy_kcal_100g": 30, "protein_per_100g": 2.1, "fat_per_100g": 0.2, "cholesterol_per_100g": 1, "carbs_per_100g": 6.6},
            {"name": "かぶ", "energy_kcal_100g": 20, "protein_per_100g": 2.3, "fat_per_100g": 0.1, "cholesterol_per_100g": 1, "carbs_per_100g": 3.9},
        ]

        for data in food_data:
            food = Food.query.filter_by(name=data["name"]).first()
        # データベースにデータを追加

            if food:
                # レコードが見つかったので更新します
                food.energy_kcal_100g = data["energy_kcal_100g"]
                food.protein_per_100g = data["protein_per_100g"]
                food.fat_per_100g = data["fat_per_100g"]
                food.cholesterol_per_100g = data["cholesterol_per_100g"]
                food.carbs_per_100g = data["carbs_per_100g"]
                food.updated_at = datetime.utcnow()
            else:

                food = Food(
                    name=data["name"],
                    energy_kcal_100g=data["energy_kcal_100g"],
                    protein_per_100g=data["protein_per_100g"],
                    fat_per_100g=data["fat_per_100g"],
                    cholesterol_per_100g=data["cholesterol_per_100g"],
                    carbs_per_100g=data["carbs_per_100g"],
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
                db.session.add(food)
        # セッションの変更をコミット
        db.session.commit()
        print("Food data added successfully!")
except Exception as e:
    print(f"An error occurred: {e}")

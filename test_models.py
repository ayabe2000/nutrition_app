import unittest
from models import get_food_by_name, create_new_food_entry, Food
from app import create_app, db

class TestFoodFunctions(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_food_by_name(self):
        with self.app.app_context():
            food_name = "Test Food"
            test_food = Food(name=food_name)
            db.session.add(test_food)
            db.session.commit()
            
            food = get_food_by_name(food_name)
            self.assertIsNotNone(food)
            self.assertEqual(food.name, food_name)

    def test_create_new_food_entry(self):

        with self.app.app_context():
            food_name = "Test Food"
            test_food = Food(name=food_name)
            db.session.add(test_food)
            db.session.commit()
            
            food = get_food_by_name(food_name)
            self.assertIsNotNone(food)

            food_entry = create_new_food_entry(food, grams=100, user_id=1, selected_date="2023-09-26")
            self.assertIsNotNone(food_entry)
            self.assertEqual(food_entry.food_name, food_name)

if __name__ == '__main__':
    unittest.main()

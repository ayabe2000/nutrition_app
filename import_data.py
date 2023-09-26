import sys
import pandas as pd
import logging
from app import db, create_app
from models import Food,convert_to_float
import sqlite3

logging.basicConfig(filename="import_food.log", level=logging.INFO)

def convert_to_float(value):
    """Convert the given value to float. If the conversion fails, return 0.0."""
    try:
        if isinstance(value, (int, float)):
            return float(value)
        elif isinstance(value, str):
            # Handle strings that might represent numbers
            cleaned_value = value.replace(",", "").replace("(", "").replace(")", "").replace("Tr", "").strip()
            if cleaned_value:
                return float(cleaned_value)
            else:
                return 0.0
        else:
            return 0.0
    except ValueError:
        return 0.0

def process_row(row):
    """Excelのデータを処理するコード"""
    # 食品名
    food_name = row["食品名"]
    # エネルギー（kcal）
    energy_val = convert_to_float(row["エネルギー（kcal）"])
    # たんぱく質
    protein_val = convert_to_float(row["たんぱく質"])
    # 脂質
    fat_val = convert_to_float(row["脂質"])
    # コレステロール
    cholesterol_val = convert_to_float(row["コレステロール"])
    # 炭水化物
    carbohydrates_val = convert_to_float(row["炭水化物"])

    if not Food.query.filter_by(name=food_name).first():
        new_food = Food(
            name=food_name,
            protein_per_100g=protein_val,
            carbs_per_100g=carbohydrates_val,
            fat_per_100g=fat_val,
            cholesterol_per_100g=cholesterol_val,
            energy_kcal_100g=energy_val,
        )
        db.session.add(new_food)
        db.session.commit()
        logging.info(f"Added food: {food_name}")

def import_to_sqlite(excel_file_path, db_path="instance/nutrition_app.db"):
    # Excelファイルの読み込み
    data = pd.read_excel(excel_file_path, skiprows=3, header=[0, 1])
    print(data.columns)
   
    # カラムの選択と名前の変更
    selected_columns = [
        ('Unnamed: 3_level_0', '食品名'),
        ('Unnamed: 5_level_0', '廃 棄 率'),
        ('Unnamed: 8_level_0', '一般成分'),
        ('Unnamed: 10_level_0', '一般成分'),
        ('Unnamed: 15_level_0', '一般成分'),
        ('Unnamed: 16_level_0', '一般成分')
    ]

    selected_data = data[selected_columns]
    selected_data.columns = ['name', 'energy_kcal_100g', 'protein_per_100g', 'fat_per_100g', 'cholesterol_per_100g', 'carbs_per_100g']
    
    # SQLiteに接続
    conn = sqlite3.connect(db_path)
    
    # データの挿入
    selected_data.to_sql('food', conn, if_exists='append', index=False)
    
    # 接続のクローズ
    conn.close()

if __name__ == "__main__":
    # コマンドライン引数の確認
    if len(sys.argv) != 2:
        print("Usage: python import_data.py <path_to_excel_file>")
        sys.exit(1)

    excel_path = sys.argv[1]
    import_to_sqlite(excel_path)

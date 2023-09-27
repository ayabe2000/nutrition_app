"""データベースにデータを追加し、そのデータを取得してグラフ化し、そのグラフをHTMLファイルに埋め込む"""
from sqlalchemy import create_engine, text
from flask import current_app as app

import matplotlib.pyplot as plt
import base64
from datetime import datetime

from models import Food
from io import BytesIO


foods = [
    {
        "name": "こむぎ",
        "protein_per_100g": 10.6,
        "carbs_per_100g": 72.2,
        "fat_per_100g": 10.6,
        "cholesterol_per_100g": 1,
        "energy_kcal_100g": 337,
    },
    {
        "name": "食パン",
        "protein_per_100g": 9.3,
        "carbs_per_100g": 46.7,
        "fat_per_100g": 4.4,
        "cholesterol_per_100g": 1,
        "energy_kcal_100g": 264,
    },
    {
        "name": "うどん",
        "protein_per_100g": 6.1,
        "carbs_per_100g": 56,
        "fat_per_100g": 0.8,
        "cholesterol_per_100g": 1,
        "energy_kcal_100g": 270,
    },
    {
        "name": "こめ",
        "protein_per_100g": 6.8,
        "carbs_per_100g": 74.3,
        "fat_per_100g": 2.7,
        "cholesterol_per_100g": 1,
        "energy_kcal_100g": 353,
    },
    {
        "name": "いも",
        "protein_per_100g": 1.9,
        "carbs_per_100g": 14.7,
        "fat_per_100g": 0.4,
        "cholesterol_per_100g": 1,
        "energy_kcal_100g": 35,
    },
    {
        "name": "あずき",
        "protein_per_100g": 20.3,
        "carbs_per_100g": 6.6,
        "fat_per_100g": 0.2,
        "cholesterol_per_100g": 1,
        "energy_kcal_100g": 339,
    },
    {
        "name": "オクラ",
        "protein_per_100g": 2.1,
        "carbs_per_100g": 6.6,
        "fat_per_100g": 0.2,
        "cholesterol_per_100g": 1,
        "energy_kcal_100g": 30,
    },
    {
        "name": "かぶ",
        "protein_per_100g": 2.3,
        "carbs_per_100g": 3.9,
        "fat_per_100g": 0.2,
        "cholesterol_per_100g": 1,
        "energy_kcal_100g": 30,
    },
]

def fetch_data(user_id):
    """データベースから日付ごとの栄養素摂取量を取得"""


    engine = create_engine("sqlite:///instance/nutrition_app.db")

    connection = engine.connect()
    result = connection.execute(
        text("SELECT date, SUM(protein) as protein, SUM(energy_kcal) as energy, SUM(fat) as fat, SUM(cholesterol) as cholesterol, SUM(carbohydrates) as carbohydrates FROM food_entry WHERE date IS NOT NULL AND user_id = :user_id GROUP BY date"),
        {'user_id': user_id}
    )

    dates = []
    protein = []
    energy = []
    fat = []
    cholesterol = []
    carbohydrates = []

    for row in result:

        date_str = row[0]
        if date_str:

            dates.append(datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f'))     

        else:
            dates.append(None)


        protein.append(row[1])
        energy.append(row[2])
        fat.append(row[3])
        cholesterol.append(row[4]) 
        carbohydrates.append(row[5])  



    connection.close()

    return dates, protein, energy, fat, cholesterol, carbohydrates


def generate_graph(dates, protein, energy, fat, cholesterol, carbohydrates):
    """fetch_data関数から取得したデータを用いて栄養素摂取量の時間経過による変化を示すグラフを作成"""

    fig,axes =plt.subplots(3,2,figsize=(10,10))

    axes[0,0].plot(dates,protein,label="Protein(g)",color="b")
    axes[0,0].set_title("Protein Intake Over Time")
    axes[0,0].set_xlabel("Date")
    axes[0,0].set_ylabel("Protein (g)")
    axes[0,0].tick_params(axis="x",rotation=45)

    axes[0,1].plot(dates,energy,label="Energy (kcal)",color="g")
    axes[0,1].set_title("Energy Intake Over Time")
    axes[0,1].set_xlabel("Date")
    axes[0,1].set_ylabel("Energy (kcal)")
    axes[0,1].tick_params(axis="x",rotation=45)
    
    axes[1,0].plot(dates,protein,label="Fat(g)",color="r")
    axes[1,0].set_title("Fat Intake Over Time")
    axes[1,0].set_xlabel("Date")
    axes[1,0].set_ylabel("Fat (g)")
    axes[1,0].tick_params(axis="x",rotation=45)

    axes[1, 1].plot(dates, cholesterol, label="Cholesterol (mg)", color='c')
    axes[1, 1].set_title("Cholesterol Intake Over Time")
    axes[1, 1].set_xlabel("Date")
    axes[1, 1].set_ylabel("Cholesterol (mg)")
    axes[1, 1].tick_params(axis='x', rotation=45)

    axes[2, 0].plot(dates, carbohydrates, label="Carbohydrates (g)", color='m')
    axes[2, 0].set_title("Carbohydrates Intake Over Time")
    axes[2, 0].set_xlabel("Date")
    axes[2, 0].set_ylabel("Carbohydrates (g)")
    axes[2, 0].tick_params(axis='x', rotation=45)

    fig.delaxes(axes[2,1])


    with BytesIO() as buffer:
        plt.savefig(buffer, format='png')
        buffer.seek(0)




        img_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    return img_base64





def get_image_data(user_id):
    """fetch_data, generate_graph, get_base64_encoded_image,create_html関数を順番に呼び出し、プロセスを実行"""

    dates, protein, energy, fat, cholesterol, carbohydrates = fetch_data(user_id)
    encoded_image =generate_graph(dates, protein, energy, fat, cholesterol, carbohydrates)



    return encoded_image




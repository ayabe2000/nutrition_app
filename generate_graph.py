"""データベースにデータを追加し、そのデータを取得してグラフ化し、そのグラフをHTMLファイルに埋め込む"""
from sqlalchemy import create_engine, text
from flask import current_app as app
import matplotlib.pyplot as plt
import base64
from datetime import datetime
from io import BytesIO




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
    plt.figure()
    plt.plot(dates, protein, label="Protein (g)")
    plt.plot(dates, energy, label="Energy (kcal)")
    plt.plot(dates, fat, label="Fat (g)")
    plt.plot(dates, cholesterol, label="Cholesterol (mg)")
    plt.plot(dates, carbohydrates, label="Carbohydrates (g)")

    plt.title("Nutrient Intake Over Time")
    plt.xlabel("Date")
    plt.ylabel("Intake")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()


    with BytesIO() as buffer:
        plt.savefig(buffer, format='png')
        buffer.seek(0)




        img_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    return img_base64





def get_image_data(user_id):
    """fetch_data, generate_graph, get_base64_encoded_image,create_html関数を順番に呼び出し、プロセスを実行"""

    dates, protein, energy, fat, cholesterol, carbohydrates = fetch_data(user_id)
    encoded_image=generate_graph(dates, protein, energy, fat, cholesterol, carbohydrates)



    return encoded_image




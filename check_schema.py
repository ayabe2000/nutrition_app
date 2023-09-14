import sqlite3

# Step 1: データベースへの接続を開く
conn = sqlite3.connect("/root/nutrition_app4/database.db")

# Step 2: カーソルオブジェクトを作成
cursor = conn.cursor()

# Step 3: 日付範囲内でデータを選択する
cursor.execute("SELECT * FROM food WHERE date BETWEEN '2023-09-03' AND '2023-09-12'")
rows = cursor.fetchall()

# Step 4: 結果を確認する
if rows:
    for row in rows:
        print(row)
else:
    print("No data found for the given date range")

# Optional Step 5: データベース内のテーブル名を取得
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
table_names = cursor.fetchall()
print("List of tables in the database:")
for table_name in table_names:
    print(table_name)

# Step 6: データベース接続を閉じる
conn.close()

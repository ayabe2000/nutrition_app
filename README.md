# Nutrition App

このプロジェクトは栄養素情報を管理するためのアプリケーションです。

## 動作環境

このプロジェクトを実行するためには以下の環境が必要です：

- Python 3.10.12
- Flask 2.3.3
- Werkzeug 2.3.7

## インストールとセットアップ

プロジェクトのセットアップ手順を詳細に説明します。以下は一般的な手順の例です。

1. プロジェクトのクローン

   ```bash
   git clone https://github.com/ayabe2000/nutrition_app.git
   cd nutrition_app

2,仮想環境の作成とアクティベーション

    python -m venv venv
    source venv/bin/activate

3,依存ライブラリのインストール

    pip install -r requirements.txt

4,データベースのセットアップ

    flask db migrate
    flask db upgrade


5,サーバーの起動

    flask run

6,ブラウザへ移動

    http://127.0.0.1:5000


## DBの栄養素情報の登録方法

このプロジェクトでは、文部科学省が提供している日本食品標準成分表2015年版（七訂）第2章　日本食品標準成分表　Exceｌ（日本語版）を使用しています。

https://www.mext.go.jp/a_menu/syokuhinseibun/1365420.htm

Excelファイルは準備したExcelパスに置き換える必要があります。

1. Excelファイルの準備:
   
   - 栄養素情報を含むExcelファイルを用意します。
   - Excelファイルのカラムには、必要な栄養素情報（食品名、カロリー、たんぱく質、脂質、炭水化物）が含まれている必要があります。


2. データの取り込み:

   - プロジェクトのルートディレクトリに移動し、仮想環境をアクティベートします。

     source venv/bin/activate

   - コマンドラインから以下のコマンドを実行してスクリプトを直接実行します
   　Excelパスは準備したものに置き換えます。
     
     python import_data.py xxxx.xlsx

   - データの取り込みが完了すると、栄養素情報がデータベースに登録されます。

3. 確認方法
  
   - 取り込みが成功したら、SQLiteコマンドを使用してデータベースをクエリし、データが正しくインポートされたことを確認します。

   sqlite3 instance/nutrition_app.db

   SELECT * FROM food;


これで、Excelファイルから栄養素情報をデータベースに登録できます。
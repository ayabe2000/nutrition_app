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

    flask db init
    flask db migrate
    flask db upgrade

'flask db init'コマンドは新しいマイグレーションリポジトリを初期化しますが、
既存の'migrations'ディレクトリが問題を引き起こす可能性があります。
その場合は、既存の'migrations'ディレクトリをバックアップまたはリネームします。

mv migrations migrations_backup

5,サーバーの起動

    flask run

6,ブラウザへ移動

    http://127.0.0.1:5000




## DBの栄養素情報の登録方法

このプロジェクトでは、栄養素情報をデータベースに登録するために以下の手順を使用します。栄養素情報は通常、Excelファイルから取り込むことが一般的です。

1. Excelファイルの準備:
   
   - 栄養素情報を含むExcelファイルを用意します。
   - Excelファイルのカラムには、必要な栄養素情報（食品名、カロリー、たんぱく質、脂質、炭水化物）が含まれている必要があります。

2. データの取り込み:

   - プロジェクトのルートディレクトリに移動し、仮想環境をアクティベートします。

     source venv/bin/activate
   
   - コマンドラインから独立して実行することができるように設計されています。
   - 以下の手順でExcelファイルからデータをデータベースに取り込みます。ファイル名やパスは実際のファイルに合わせて変更してください。
   - コマンドラインから以下のコマンドを実行してスクリプトを直接実行します
   - Flaskアプリケーションを起動します。app.py 内で app.run(debug=True) を呼び出すことで、アプリケーションが実行されます。その後、別のターミナルで flask import-nutrition-data を実行できます。


   - コマンドラインから以下のコマンドを実行してスクリプトを直接実行します
     
     python import_data.py

   - 新しいターミナルウィンドウを開きます。
     
   - Flaskアプリケーションを起動するために、以下のコマンドを実行します。これにより、アプリケーションがバックグラウンドで実行されます。

     flask run
  
   - 別のターミナルウィンドウを開き、以下のコマンドを使用して「flask import-nutrition-data」を実行します。
  
     flask import-nutrition-data /mnt/c/Users/user/Downloads/food_data.xlsx


   - データの取り込みが完了すると、栄養素情報がデータベースに登録されます。
  
   - 取り込みが成功したら、SQLiteコマンドを使用してデータベースをクエリし、データが正しくインポートされたことを確認します。

これで、Excelファイルから栄養素情報をデータベースに登録できます。
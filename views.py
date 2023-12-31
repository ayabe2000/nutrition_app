"""FlaskやDjangoといったPythonのウェブフレームワークにおいて、ウェブアプリケーションの"ビュー"層を定義"""
from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, request, flash,session
from flask_login import login_user, current_user
from sqlalchemy import or_
from forms import LoginForm, RegistrationForm, FoodEntryForm, EditGramsForm
from models import (
    User,
    FoodEntry,
    Food,
    DailyNutrient,
    db,
    create_new_food_entry,
)
from models import create_new_food_entry


from generate_graph import get_image_data
import jaconv


main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def index():
    """indexのルート関数"""

    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("main.login_page"))


@main_blueprint.route("/login", methods=["GET", "POST"])
def login_page():
    """roginのルート関数"""
    login_form = LoginForm()
    register_form = RegistrationForm()

    if request.method == "POST":
        if "submit_login" in request.form:
            if login_form.validate_on_submit():
                user = User.query.filter_by(username=login_form.username.data).first()
                if user:
                    if user and user.check_password(login_form.password.data):
                        login_user(user)
                        session['user_id'] = user.id
                        return redirect(url_for("main.dashboard"))
        elif "submit_register" in request.form:
            if register_form.validate_on_submit():
                existing_user = User.query.filter_by(
                    username=register_form.new_username.data
                ).first()
                if existing_user:
                    return render_template(
                        "login.html",
                        login_form=login_form,
                        register_form=register_form,
                        message="Username already exists.",
                    )

                new_user = User(username=register_form.new_username.data)
                new_user.set_password(register_form.new_password.data)

                db.session.add(new_user)
                db.session.commit()

                login_user(new_user)
                session['user_id'] = new_user.id 
                return redirect(url_for("main.dashboard"))
    return render_template(
        "login.html", login_form=login_form, register_form=register_form
    )

@main_blueprint.route('/logout',methods=['POST'])
def logout():
    session.clear() 
    return redirect(url_for('main.login_page')) 



@main_blueprint.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    """フォームデータの取得と処理"""
    form = FoodEntryForm()
    nutrients_data_today = None
    selected_date = form.date.data

    user_id = session.get('user_id')


    if form.validate_on_submit() and current_user.is_authenticated:

        response_data = handle_form_submission(form)

        if "error" not in response_data:
            nutrients_data_today = response_data

        else:
            print(response_data["error"])

      

    selected_food_nutrients = FoodEntry.query.filter(FoodEntry.user_id == user_id).all()
    nutrients_data = compute_nutrients(selected_food_nutrients)
    entries = group_entries_by_date(selected_food_nutrients)



    encoded_image = get_image_data(user_id)


    return render_template(
        "dashboard.html",
        form=form,
        nutrients_data_today=nutrients_data_today,
        nutrients_data=nutrients_data,
        entries=entries,
        selected_date=selected_date,
        encoded_image = get_image_data(user_id)
    )


def handle_form_submission(form):
    """食品データベースから食品の取得"""
    food_name = form.name.data
    print("food_name:", food_name)
    grams = form.grams.data
    selected_date = form.date.data

    food = Food.query.filter(Food.name == food_name).first()
    print("food:", food)

    if food:
        user_id = current_user.id
        selected_date = form.date.data
        new_entry = create_new_food_entry(
            food, grams, user_id, selected_date
        )

        if new_entry is None:
            return {"error": "Failed to create a new food entry."}

        db.session.add(new_entry)
        db.session.commit()

        today = datetime.utcnow().date()
        nutrients_data_today = get_nutrients_data_today(today)

        update_daily_nutrient(user_id, nutrients_data_today, selected_date)

        return nutrients_data_today

    return {"error": "Food not found in the database"}


def get_nutrients_data_today(today):
    """今日の栄養データの計算"""
    end_of_today = today + timedelta(days=1) - timedelta(seconds=1)
    today_entries = FoodEntry.query.filter(
        FoodEntry.date.between(today, end_of_today)
    ).all()
    return compute_nutrients(today_entries)


def update_daily_nutrient(user_id, nutrients_data_today, selected_date):
    """デイリーナットリエントの作成/更新"""
    daily_nutrient = DailyNutrient.query.filter_by(
        user_id=user_id, date=selected_date
    ).first()
    if not daily_nutrient:
        daily_nutrient = DailyNutrient(date=selected_date, user_id=user_id)
        db.session.add(daily_nutrient)

    daily_nutrient.total_protein = nutrients_data_today["Protein"]
    daily_nutrient.total_carbs = nutrients_data_today["Carbohydrates"]
    daily_nutrient.total_fat = nutrients_data_today["Fat"]

    db.session.commit()


def compute_nutrients(entries, debug_mode=False):
    """全エントリーの取得と栄養データの計算"""
 
    nutrients_data = {
        "Protein": 0,
        "Carbohydrates": 0,
        "Fat": 0,
        "Cholesterol": 0,
        "Energy_kcal": 0,
    }

    for entry in entries:
        if isinstance(entry, FoodEntry):
            entry_dict = {
                "protein": entry.protein,
                "carbohydrates": entry.carbohydrates,
                "fat": entry.fat,
                "cholesterol": entry.cholesterol,
                "energy_kcal": entry.energy_kcal,
            }
            required_keys = [
                "protein",
                "carbohydrates",
                "fat",
                "cholesterol",
                "energy_kcal",
            ]
        elif isinstance(entry, dict):
            entry_dict = entry
            required_keys = [
                "protein",
                "carbohydrates",
                "fat",
                "cholesterol",
                "energy_kcal",
            ]
        else:
            raise ValueError("Invalid entry format detected.")

        if not all(key in entry_dict for key in required_keys):
            raise ValueError("Invalid entry format detected.")

        if debug_mode:
            print("Entry:", entry_dict)

        nutrients_data["Protein"] += entry_dict["protein"]
        nutrients_data["Carbohydrates"] += entry_dict["carbohydrates"]
        nutrients_data["Fat"] += entry_dict["fat"]
        nutrients_data["Cholesterol"] += entry_dict["cholesterol"]
        nutrients_data["Energy_kcal"] += entry_dict["energy_kcal"]

    if debug_mode:
        print("Nutrients Data:", nutrients_data)

    return nutrients_data


def group_entries_by_date(all_entries):
    """グループ化されたエントリーの作成"""

    grouped_entries = {}
    for entry in all_entries:
        date_str = entry.date.strftime("%Y-%m-%d")
        if date_str not in grouped_entries:
            if len(grouped_entries) >= 10:  # 10日分のデータのみ保持
                oldest_entry_key = list(grouped_entries.keys())[0]  # 最も古いエントリのキーを取得
                grouped_entries.pop(oldest_entry_key)  # 最も古いエントリを削除
            grouped_entries[date_str] = {
                "kcal": 0,
                "protein": 0,
                "fat": 0,
                "cholesterol": 0,
                "carbs": 0,
                "foods": [],
            }

        grouped_entries[date_str]["kcal"] += entry.energy_kcal
        grouped_entries[date_str]["protein"] += entry.protein
        grouped_entries[date_str]["fat"] += entry.fat
        grouped_entries[date_str]["cholesterol"] += entry.cholesterol
        grouped_entries[date_str]["carbs"] += entry.carbohydrates
        grouped_entries[date_str]["foods"].append(entry)

    entries = []
    for date_str, data in grouped_entries.items():
        entries.append(
            {
                "date": date_str,
                "kcal": f"{data['kcal']} kcal",
                "protein": f"{data['protein']} g",
                "fat": f"{data['fat']} g",
                "cholesterol": f"{data['cholesterol']} mg",
                "carbs": f"{data['carbs']} g",
                "foods": data["foods"],
            }
        )
    return entries


@main_blueprint.route("/edit_food/<int:id>", methods=["GET", "POST"])
def edit_food(id):
    """食品エントリの編集"""
    entry = FoodEntry.query.get(id)
    form = EditGramsForm()
    print("Entry:", entry)

    if request.method == "POST":
        new_grams = request.form.get("grams")
        if new_grams:
            entry.grams = new_grams
            db.session.commit()
            return redirect(url_for("main.dashboard"))
        else:
            error_message = "新しいグラム数を入力してください"
    else:
        error_message = ""
        
    target_date = entry.date.date()
    target_datetime_start = datetime.combine(target_date, datetime.min.time())
    target_datetime_end = datetime.combine(target_date, datetime.max.time())

    food_entries = FoodEntry.query.filter(
        FoodEntry.user_id == entry.user_id, 
        FoodEntry.date >= target_datetime_start, 
        FoodEntry.date <= target_datetime_end
    ).all()




    print("Entry object before render_template:", entry)
    return render_template(
        "edit_food.html", entry=entry, error_message=error_message, form=form,food_entries=food_entries
    )


@main_blueprint.route("/delete_food/<int:id>", methods=["POST"])
def delete_food(id):
    """食品エントリの削除"""
    entry = FoodEntry.query.get(id)
    if entry:
        db.session.delete(entry)
        db.session.commit()
        flash("エントリが正常に削除されました", "success")
    else:
        flash("エントリが見つかりません", "error")
    return redirect(url_for("main.dashboard"))


@main_blueprint.route('/search_food')
def search_food():
    query = request.args.get('query')  # クエリパラメータを取得

    if query:
        hiragana_query = jaconv.kata2hira(query)
        results = Food.query.filter(
            or_(
            Food.name.like(f'%{query}%'), # カタカナの検索
            Food.name.like(f'%{hiragana_query}%')  # ひらがなの検索
            )
        ).all()
            
    else:
        results = []  # クエリが指定されていない場合、空のリストを使用

    # 検索結果を search_results.html テンプレートに渡す
    return render_template('search_results.html', results=results)


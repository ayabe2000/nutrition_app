"""This module contains form classes used in the application."""
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    HiddenField,
    IntegerField,
    SelectField,
)
from wtforms.validators import DataRequired, NumberRange
from wtforms.fields import DateField
from datetime import datetime
from models import Food


class LoginForm(FlaskForm):
    """This class represents a form for user login with necessary fields and validators."""

    username = StringField("ユーザ名", validators=[DataRequired()])
    password = PasswordField("パスワード", validators=[DataRequired()])
    submit = SubmitField("ログイン")
    # トークンを保持するための非表示フィールド
    csrf_token = HiddenField(validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    """このクラスは新規登録フォームです"""

    new_username = StringField("New Username", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[DataRequired()])
    submit = SubmitField("Register")


class FoodEntryForm(FlaskForm):
    """このクラスは食品を追加する際のフォームです"""

    date = DateField("Select Date", format="%Y-%m-%d", default=datetime.today)
    name = SelectField("Select Food", choices=[])
    grams = IntegerField("Grams", validators=[NumberRange(min=1)])
    submit_entry = SubmitField("Submit")


    def __init__(self, *args, **kwargs):
        super(FoodEntryForm, self).__init__(*args, **kwargs)
        self.name.choices = [(food.name, food.name) for food in Food.query.all()]


class EditGramsForm(FlaskForm):
    grams = IntegerField(
        "新しいグラム数:", validators=[DataRequired(message="新しいグラム数を入力してください")]
    )
    submit = SubmitField("更新")

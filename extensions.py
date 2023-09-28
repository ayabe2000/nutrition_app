from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = 'sqlite:///instance/nutrition_app.db'
db = SQLAlchemy(app)

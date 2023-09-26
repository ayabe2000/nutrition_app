"""This module contains the configuration settings for the application."""
import os
SECRET_KEY = "your_secret_key"
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "instance/nutrition_app.db")

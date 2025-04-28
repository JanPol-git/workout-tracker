import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

basedir = Path(__file__).parent.parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(basedir / 'instance' / 'app.db')  # Путь к БД
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
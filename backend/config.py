import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma-chave-secreta-muito-dificil-de-adivinhar'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'postgresql://trading_bot_user:password@localhost/trading_bot_db?client_encoding=utf8'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://trading_bot_user:password@localhost/trading_bot_db?client_encoding=utf8')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


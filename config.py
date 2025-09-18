import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'NEVERMIND1991')

    # Prefer Render DATABASE_URL, fallback to local
    DATABASE_URL = os.getenv('DATABASE_URL') or os.getenv('LOCAL_DATABASE_URL')

    if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
        SQLALCHEMY_DATABASE_URI = DATABASE_URL + "?sslmode=require"
    else:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL

    SQLALCHEMY_TRACK_MODIFICATIONS = False

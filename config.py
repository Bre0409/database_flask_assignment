import os

class Config:
    # Secret key for Flask sessions
    SECRET_KEY = os.getenv('SECRET_KEY', 'NEVERMIND1991')

    # Use Render's DATABASE_URL if available
    DATABASE_URL = os.getenv('DATABASE_URL')

    if DATABASE_URL:
        # Enforce SSL for Render Postgres
        SQLALCHEMY_DATABASE_URI = DATABASE_URL + "?sslmode=require"
    else:
        # fallback to local Postgres
        SQLALCHEMY_DATABASE_URI = "postgresql://flaskuser:mypassword123@localhost/mydiary"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

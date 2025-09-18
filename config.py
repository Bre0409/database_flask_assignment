import os

class Config:
    # Secret key for Flask sessions
    SECRET_KEY = os.getenv('SECRET_KEY', 'NEVERMIND1991')

    # Database URL: prefer Render's DATABASE_URL, fallback to local Postgres
    DATABASE_URL = os.getenv('DATABASE_URL') or (
        "postgresql://bren:M4DR6dS5WPcTAMI5OhcXTJruucoz72RA@"
        "dpg-d3676n3e5dus73fqg5v0-a.frankfurt-postgres.render.com/"
        "databaseassignment_q974"
    )

    # Enforce SSL for Render Postgres
    if DATABASE_URL.startswith("postgresql://"):
        SQLALCHEMY_DATABASE_URI = DATABASE_URL + "?sslmode=require"
    else:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL

    SQLALCHEMY_TRACK_MODIFICATIONS = False

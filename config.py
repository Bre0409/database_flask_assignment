import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Secret key
    SECRET_KEY = os.getenv('SECRET_KEY', 'NEVERMIND1991')

    # Database URI: prefer Render (prod), fallback to local (dev)
    SQLALCHEMY_DATABASE_URI = (
        os.getenv('DATABASE_URL') or
        os.getenv('LOCAL_DATABASE_URL') or
        'postgresql://flaskuser:mypassword123@localhost/mydiary'
    )

    # Track modifications
    SQLALCHEMY_TRACK_MODIFICATIONS = False

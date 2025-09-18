import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Secret key
    SECRET_KEY = os.getenv('SECRET_KEY', 'NEVERMIND1991')

    # Database URI: prefer Render for prod, fallback to local for dev
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'RENDER_DATABASE_URL',
        os.getenv('LOCAL_DATABASE_URL', 'postgresql://flaskuser:mypassword123@localhost/mydiary')
    )

    # Track modifications
    SQLALCHEMY_TRACK_MODIFICATIONS = False

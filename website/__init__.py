import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Secret key
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'NEVERMIND1991')

    # Prefer Render's DATABASE_URL (Render sets this automatically for Postgres)
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # Fallback to local database (Postgres or SQLite)
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
            "LOCAL_DATABASE_URL",
            "postgresql://flaskuser:mypassword123@localhost/mydiary"
        )

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize DB and migrations
    db.init_app(app)
    migrate.init_app(app, db)

    
    # Register blueprints
    from .views import views
    from .auth import auth
    from .events import events_bp

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(events_bp, url_prefix='/')

    return app

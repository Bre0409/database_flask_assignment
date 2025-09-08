# website/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'

    # ✅ Use DATABASE_URL if set, otherwise default to Postgres
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            "postgresql://flaskuser:mypassword123@localhost/mydiary"
        )

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Init DB + migrations
    db.init_app(app)
    migrate.init_app(app, db)

    # Blueprints
    from .views import views
    from .auth import auth
    from .events import events_bp
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(events_bp, url_prefix='/')

    return app

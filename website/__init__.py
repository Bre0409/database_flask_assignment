from flask import Flask

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'Ihope Ipass thisAssigment'

    from .views import views
    from .auth import auth
    from .events import events_bp

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(events_bp, url_prefix='/')

    return app

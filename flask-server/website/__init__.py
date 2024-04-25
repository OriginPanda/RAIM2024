from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from os import path 
from flask_login import LoginManager
from flask_migrate import Migrate


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    """
    Fukncja tworząca aplikacje hosta
    """

    app = Flask(__name__)
    
    
    
    app.config['SECRET_KEY'] = 'Siemano2137'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SECURITY_REGISTERABLE'] = True
    app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
    
    migrate = Migrate(app, db) # python -m flask --app main.py db init #flask db upgrade
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    

    from .views import views
    from .auth import auth
    from .settings import settings
    from .models import User, Comment, Patient, MedicalData
    
    
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    app.register_blueprint(settings,url_prefix='/')

    with app.app_context():
        db.create_all()
    
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    
    
    
    return app


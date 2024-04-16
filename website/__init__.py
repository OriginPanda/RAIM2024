from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    """
    Fukncja tworząca aplikacje hosta
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Siemano2137'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    
    from .views import views
    from .auth import auth
    from . import models
    
    
    
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    create_DB(app)
    
    return app


def create_DB(app):
    if not path.exists('website/'+DB_NAME):
        db.create_all(app=app)
        print('Database created')

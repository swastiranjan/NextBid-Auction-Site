#__init__.py makes the website folder a python package and we can import the folder 

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'AHKcaksbv HASVabas' #this encrypts or secures the cookies and session data related to the website
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    db.init_app(app) #initalising database by giving it our flask app

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Listing, Biddings

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' #where should flask redirect if the user is not logged in
    login_manager.init_app(app) #tells the login manager which app we are using
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app 

def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print("Created database!")
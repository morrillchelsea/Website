'''
Created on Jul 4, 2022

@author: chelseanieves
'''
import logging
import socket
from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# create logger name and object
logger = logging.getLogger(__name__)
LOG_NAME = "./log.txt"
# create database name and object
db = SQLAlchemy()
DB_NAME = "database.db"
class Website(object):
    '''Doc string'''
    def __init__(self, level):
        ''' Declare instance variable'''
        self.__level = level
    def filter(self, log_record):
        ''' Error level number = 40. Filter out instance levels less than set level '''
        return log_record.levelno <= self.__level
def create_app():
    '''Creates application, configures database and blueprints for app'''
    app=Flask(__name__)
    app.config['SECRET_KEY'] = "secret key"
    # tell flask where to store db
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # pass flask app to database
    db.init_app(app)
    from .views import views # import and register additional modules/blueprints
    from .auth import auth # import and register additional modules/blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    # call method to create database
    create_database(app)
    # call method to create logger
    create_logger()
    from .models import User # import database schema
    login_manager = LoginManager()
    # redirect user to login page if not logged in
    login_manager.login_view = 'auth.login'
    # pass application to login_manager
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(id):
        '''Callback used to reload the user object from the user ID stored in the session'''
        return User.query.get(int(id))
    return app
def create_database(app):
    '''Function to validate whether a database has been created. Creates a new database
    (database.db) if it does not already exist'''
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print("Database created")
def create_logger():
    '''Create and modify logger'''
    # set level to log only ERROR and below
    logger.setLevel(logging.ERROR)
    # assign path to store logs
    handler = logging.FileHandler(f'{LOG_NAME}')
    # assign handler to logger
    logger.addHandler(handler)
    # getting the hostname by socket.gethostname() method
    hostname = socket.gethostname()
    # getting the IP address using socket.gethostbyname() method
    ip_address = socket.gethostbyname(hostname)
    ## printing the hostname and ip_address
    formatter = logging.Formatter(f'{ip_address} - %(asctime)s - %(levelname)s-%(name)s-\
    %(message)s')
    # apply formatter to logger handler
    handler.setFormatter(formatter)
    # apply filter to handler
    handler.addFilter(logger)
    
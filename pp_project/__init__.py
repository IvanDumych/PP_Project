from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth
import config

# init app
app = Flask(__name__)
app.config.from_object('config.TestingConfig')
# app.config.from_object('config.DevelopmentConfig')
auth = HTTPBasicAuth()

# Database
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
Session = sessionmaker(bind=engine)

# bcrypt
bcrypt = Bcrypt(app)

import pp_project.urls

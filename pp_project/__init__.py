from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth

# init app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
auth = HTTPBasicAuth()

# Database
engine = create_engine('sqlite:///test.db', echo=True)
Session = sessionmaker(bind=engine)

# bcrypt
bcrypt = Bcrypt(app)

import pp_project.urls

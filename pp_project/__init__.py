from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
engine = create_engine('sqlite:///database.db', echo=True)
Session = sessionmaker(bind=engine)

from pp_project import hello_world, models

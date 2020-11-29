from flask import Flask

app = Flask(__name__)

from pp_project import hello_world, models

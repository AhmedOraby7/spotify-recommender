import os
from flask import Flask

app_path = os.path.dirname(__file__)
app = Flask(__name__, static_folder = app_path+'/static')

from application import routes
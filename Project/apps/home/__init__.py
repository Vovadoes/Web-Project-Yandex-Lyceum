from flask import Blueprint

app_home = Blueprint('app_home', __name__, static_folder='static', template_folder='templates')

from .home import *

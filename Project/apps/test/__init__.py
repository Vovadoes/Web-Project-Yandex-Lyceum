from flask import Blueprint

app_test = Blueprint('app_test', __name__, static_folder='static', template_folder='templates')

from .login import *

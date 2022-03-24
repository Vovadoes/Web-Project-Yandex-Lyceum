from flask import Blueprint

from Project.data.db_session import global_init

app_home = Blueprint('app_home', __name__, static_folder='static', template_folder='templates')
global_init('db/db.db')

from .home import *

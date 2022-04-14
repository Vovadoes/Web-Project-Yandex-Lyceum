from flask import Blueprint

from Project.data.db_session import global_init
from Project.settings import path_db

app_home = Blueprint('app_home', __name__, static_folder='static', template_folder='templates')
# print(path_db)
global_init(path_db)

from .home import *

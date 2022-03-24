from flask import Blueprint

from Project.data.db_session import global_init
from Project.settings import path_db

app_articles = Blueprint('app_articles', __name__, static_folder='static', template_folder='templates')
global_init(path_db)

from .main import *

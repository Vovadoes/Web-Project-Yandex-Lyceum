from flask import Blueprint

import Project.data.Blocks.Block
from Project.data.db_session import global_init
from Project.settings import path_db

app_articles = Blueprint('app_articles', __name__, static_folder='static', template_folder='templates')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
global_init(path_db)

from Project.data.Blocks.Block import check
from Project.data.Blocks.settings import Blocks_lst as Blocks

print('Зарегестрированные блоки: ', ', '.join([Block.__name__ for Block in Blocks]), ';')
for block in Blocks:
    check(block)

from .home import *

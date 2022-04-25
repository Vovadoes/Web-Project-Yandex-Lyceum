import os
from loguru import logger

# Если используешь Pycharm то убрать из settings "Project"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


work_dir = 'Project'
way_db = os.path.join(os.getcwd(), 'Project', 'db')
if not os.path.isdir(way_db):
    os.makedirs(way_db)
path_db = os.path.join(way_db, 'db.db')
# Всегда в static
media_path = 'media'
default_image = os.path.join("static", "default", '1.jpg')
if not os.path.isdir(os.path.join(work_dir, 'static', media_path)):
    os.makedirs(os.path.join(work_dir, 'static', media_path))

# path_db_danila = os.path.join(os.getcwd(), 'Project', 'db', 'db_danila.db')

# При первом запуске
"""
python -m nltk.downloader omw-1.4
"""

# Чтобы запустить проект
"""
set FLASK_APP=Project/main.py
set FLASK_DEBUG=1
cls & python -m flask run --host localhost --port 8080 --reload --debugger
"""

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="10MB",
           compression="zip")

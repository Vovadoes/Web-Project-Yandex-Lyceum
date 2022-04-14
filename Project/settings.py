import os.path
from loguru import logger

# Если используешь Pycharm то убрать из settings "Project"

work_dir = 'Project'

path_db = os.path.join(os.getcwd(), 'Project', 'db', 'db.db')

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

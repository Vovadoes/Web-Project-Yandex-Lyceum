import os.path
from loguru import logger

work_dir = 'Project'

path_db = os.path.join(os.getcwd(), 'Project', 'db', 'db.db')

"""
set FLASK_APP=Project/main.py
set FLASK_DEBUG=1
cls & python -m flask run --host localhost --port 8080 --reload --debugger
"""

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="10MB",
           compression="zip")

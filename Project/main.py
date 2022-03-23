import datetime

from flask import Flask, request, make_response, session, render_template, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import CSRFProtect
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from data import db_session
from data.db_session import global_init

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    global_init("db/db.db")
    app.run(port=8080, host='localhost')

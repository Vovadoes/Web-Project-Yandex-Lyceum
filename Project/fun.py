from flask_login import current_user
from werkzeug.utils import redirect

from Project.data.User import User
from Project.data.db_session import create_session


def get_user(required=True, is_super_user=False):
    def get_user_f(function):
        def my_finished_function(*args, **kwargs):
            user = None
            db_sess = create_session()
            user_id = current_user.get_id()
            if user_id is None:
                if required:
                    return redirect("/login")
            else:
                user = db_sess.query(User).filter().first(User.id == user_id)
                if is_super_user:
                    if not user.super_user:
                        return {"error": "Not enough rights"}
            return function(user=user, *args, **kwargs)

        my_finished_function.__name__ = function.__name__
        return my_finished_function

    return get_user_f

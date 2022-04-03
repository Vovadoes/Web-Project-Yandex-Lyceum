from flask_login import current_user
from werkzeug.utils import redirect

from Project.data.User import User
from Project.data.db_session import create_session


def get_user(required=True, is_super_user=False):
    def get_user_f(function):
        def finished_function(*args, **kwargs):
            user = None
            db_sess = create_session()
            user_id = current_user.get_id()
            if user_id is None:
                if required:
                    return redirect("/login")
            else:
                user = db_sess.query(User).filter().first(User.id == user_id)
                if is_super_user:
                    # if not current_user.is_superuser:
                    #     return 'Недостаточно прав'
                    pass
            return function(user=user, *args, **kwargs)

        return finished_function

    return get_user_f

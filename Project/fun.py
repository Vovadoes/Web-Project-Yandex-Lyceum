from flask_login import current_user
from werkzeug import Response
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from Project.settings import ALLOWED_EXTENSIONS
from Project.data.Article import Article
from Project.data.User import User
from Project.data.db_session import create_session
from Project.data.Blocks.settings import Blocks_lst


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
                user = db_sess.query(User).filter(User.id == user_id).first()
                if is_super_user:
                    if not user.super_user:
                        return {"error": "Not enough rights"}
            return function(user=user, *args, **kwargs)

        my_finished_function.__name__ = function.__name__
        return my_finished_function

    return get_user_f


def user_is_author(required: bool = True):
    def get_user_f(function):
        def my_finished_function(user, article_id, *args, **kwargs):
            db_sess = create_session()
            article: Article = db_sess.query(Article).filter(Article.id == article_id).first()
            if article.user_id != user.id and required:
                return abort(404)
            return function(user=user, article_id=article_id, *args, **kwargs)

        get_user_f.__name__ += '-' + user_is_author.__name__
        my_finished_function.__name__ += '-' + get_user_f.__name__ + '-' + function.__name__
        return my_finished_function

    return get_user_f


def get_article_id(required: bool = True):
    def get_user_f(function):
        def my_finished_function(article_id, *args, **kwargs):
            if len(str(article_id)) > 20:
                return abort(404)
            db_sess = create_session()
            article: Article = db_sess.query(Article).filter(Article.id == article_id).first()
            if article is None and required:
                return {"res": "There is no article with this number"}
            return function(article_id=article_id, *args, **kwargs)

        my_finished_function.__name__ = function.__name__
        return my_finished_function

    return get_user_f


def get_block(required: bool = True):
    def get_user_f(function):
        def my_finished_function(block_id, number_block, *args, **kwargs):
            db_sess = create_session()
            if not (0 <= number_block < len(Blocks_lst)) or len(str(number_block)) > 1000000000:
                return abort(404)
            if len(str(block_id)) > 1000000000:
                return abort(404)
            block = db_sess.query(Blocks_lst[number_block]).filter(
                Blocks_lst[number_block].id == block_id
            ).first()
            if block is None and required:
                return abort(Response("Block not found"))
            return function(block_id=block_id, number_block=number_block, *args, **kwargs)

        my_finished_function.__name__ = function.__name__
        return my_finished_function

    return get_user_f

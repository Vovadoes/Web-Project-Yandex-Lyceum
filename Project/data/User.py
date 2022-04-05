import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship

from werkzeug.security import generate_password_hash, check_password_hash

from .Article import association_table_views
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'user'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    super_user = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date_create = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    article = relationship("Article", back_populates="user")
    views = relationship("Article", secondary=association_table_views, back_populates="views")

    def __init__(self, **kwargs):
        super().__init__()
        for i in kwargs:
            if i in User.__dict__.keys():
                setattr(self, i, kwargs[i])
            else:
                print(f'Error Key: {i}')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

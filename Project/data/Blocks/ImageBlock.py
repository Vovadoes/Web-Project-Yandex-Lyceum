import sqlalchemy
from Project.data.db_session import SqlAlchemyBase
from flask_login import UserMixin
from .settings import Blocks_lst

from .Block import Block


class ImageBlock(Block):
    __tablename__ = 'image_blocks'
    __table_args__ = {'extend_existing': True}

    heading = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    image_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('images.id'))


Blocks_lst.append(ImageBlock)

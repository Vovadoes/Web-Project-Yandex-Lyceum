import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import declared_attr

from .Block import Block
from .settings import Blocks_lst


class MainIdeaBlock(Block):
    __tablename__ = 'MainIdea_Block'
    __table_args__ = {'extend_existing': True}

    idea = sqlalchemy.Column(sqlalchemy.String, nullable=True)


Blocks_lst.append(MainIdeaBlock)

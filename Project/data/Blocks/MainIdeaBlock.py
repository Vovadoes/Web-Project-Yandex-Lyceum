import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import declared_attr

from .Block import Block
from .settings import Blocks_lst
from Project.forms.MainIdeaForm import MainIdeaForm


class MainIdeaBlock(Block):
    __tablename__ = 'MainIdea_Block'
    __table_args__ = {'extend_existing': True}

    idea = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    @staticmethod
    def getForm():
        return MainIdeaForm

    @staticmethod
    def label_block():
        return 'Блок с главной идеей'


Blocks_lst.append(MainIdeaBlock)

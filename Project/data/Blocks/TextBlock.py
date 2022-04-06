import sqlalchemy

from .Block import Block
from .settings import Blocks_lst


class TextBlock(Block):
    __tablename__ = 'text_blocks'
    __table_args__ = {'extend_existing': True}

    heading = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    @staticmethod
    def label_block():
        return 'Блок с текстом'


Blocks_lst.append(TextBlock)

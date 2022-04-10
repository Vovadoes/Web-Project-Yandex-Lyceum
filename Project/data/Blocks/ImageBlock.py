import sqlalchemy
from .settings import Blocks_lst

from .Block import Block
from Project.forms.Blocks.ImageForm import ImageForm


class ImageBlock(Block):
    __tablename__ = 'image_blocks'
    __table_args__ = {'extend_existing': True}

    heading = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    image_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('images.id'))

    @staticmethod
    def getForm():
        return ImageForm

    @staticmethod
    def label_block():
        return 'Блок c изображением'


Blocks_lst.append(ImageBlock)

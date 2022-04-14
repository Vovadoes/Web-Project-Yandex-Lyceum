import os

import sqlalchemy
from .settings import Blocks_lst

from .Block import Block
from Project.forms.Blocks.ImageForm import ImageForm
from Project.data.db_session import create_session
from Project.apps.articles.upload_file import allowed_file
from Project.apps.articles.upload_file import secure_filename
from Project.data.Image import Image
from Project.settings import work_dir


class ImageBlock(Block):
    __tablename__ = 'image_blocks'
    __table_args__ = {'extend_existing': True}

    heading = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    image_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('images.id'))

    def loading_data(self, request, **kwargs):
        self.import_class_dict(**kwargs)
        db_sess = create_session()
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            img = Image()
            path = img.generate_path(filename, set_path=True)
            file.save(os.path.join(os.path.join(work_dir, 'media'), path))
            db_sess.add(img)
            db_sess.commit()

    @staticmethod
    def getForm():
        return ImageForm

    @staticmethod
    def label_block():
        return 'Блок c изображением'


Blocks_lst.append(ImageBlock)

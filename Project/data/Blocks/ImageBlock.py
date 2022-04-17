import os

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import Session
from werkzeug.utils import secure_filename

from .settings import Blocks_lst

from .Block import Block
from Project.forms.Blocks.ImageForm import ImageForm
from Project.data.db_session import create_session
from Project.settings import allowed_file

from Project.data.Image import Image
from Project.settings import work_dir, media_path


class ImageBlock(Block):
    __tablename__ = 'image_blocks'
    __table_args__ = {'extend_existing': True}

    heading = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    image_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('images.id'))

    def get_image(self):
        db_sess = create_session()
        return db_sess.query(Image).filter(Image.id == self.image_id).first()

    def loading_data(self, request, db_sess, form, **kwargs):
        super(ImageBlock, self).loading_data(request, db_sess, form, **kwargs)
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            img = Image()
            path = img.generate_path(filename, set_path=True)
            file.save(os.path.join(os.path.join(work_dir, 'static', media_path), path))
            db_sess.add(img)
            return img

    def change_db(self, db_sess: Session = None, result: Image = None, *args, **kwargs):
        self.image_id = result.id
        db_sess.commit()

    def preparing_for_deletion(self, db_sess: Session = None, *args, **kwargs):
        super(ImageBlock, self).preparing_for_deletion(db_sess=db_sess, *args, **kwargs)
        image = db_sess.query(Image).filter(Image.id == self.image_id).first()
        os.remove(os.path.join(os.path.join(work_dir, 'static', media_path), image.path))
        db_sess.delete(image)


    @staticmethod
    def getForm():
        return ImageForm

    @staticmethod
    def label_block():
        return 'Блок c изображением'


Blocks_lst.append(ImageBlock)

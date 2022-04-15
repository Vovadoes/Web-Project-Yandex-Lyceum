import os

from werkzeug.utils import redirect, secure_filename

from . import app_articles, ALLOWED_EXTENSIONS

from flask import render_template, request, url_for

from Project.data.db_session import create_session
from Project.data.Image import Image
from Project.settings import work_dir


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app_articles.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        db_sess = create_session()
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            img = Image()
            path = img.generate_path(filename, set_path=True)
            file.save(os.path.join(os.path.join(work_dir, 'media'), path))
            db_sess.add(img)
            db_sess.commit()
            return redirect(url_for('app_articles.upload_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
    </form'''

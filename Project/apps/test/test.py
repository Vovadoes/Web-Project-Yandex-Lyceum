from . import app_test

from flask import render_template


@app_test.route("/")
def test():
    return render_template('base.html')

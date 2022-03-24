from . import app_test

from flask import render_template


@app_test.route("/test")
def test():
    return render_template('base.html')

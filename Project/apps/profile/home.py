from . import app_profile
from Project.fun import get_user
from flask import render_template, request


@app_profile.route("/")
@get_user(required=False)
def main(user, *args, **kwargs):
    return render_template('Profile/Main.html', user=user)
    pass
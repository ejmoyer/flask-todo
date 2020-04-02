from flask import Blueprint, render_template, request, redirect, url_for

from . import db

bp = Blueprint("auth", __name__, url_prefix='/auth')

@bp.route("/")
def login():
    return render_template("register.html")


@bp.route("/register", methods=('GET', 'POST'))
def register():
    conn = db.get_db()
    cur = conn.cursor()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

    return render_template('register.html')

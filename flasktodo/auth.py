from flask import Blueprint, render_template, request, redirect, url_for

from werkzeug.security import generate_password_hash

from . import db

bp = Blueprint("auth", __name__, url_prefix='/auth')

@bp.route("/")
def login():
    return render_template("register.html")


@bp.route("/register", methods=('GET', 'POST'))
def register():
    conn = db.get_db()
    cur = conn.cursor()
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None: # password as a hash
            cur.execute(
                'INSERT INTO users (username, password) VALUES (%s, %s)',
                (username, generate_password_hash(password))
            )
            conn.commit()
            return redirect(url_for('auth.login')) #sends user to login page

        flash(error)


    return render_template('register.html')

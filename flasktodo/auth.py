import functools

from flask import Blueprint, render_template, request, redirect, url_for, session, g

from werkzeug.security import generate_password_hash, check_password_hash

from . import db

bp = Blueprint("auth", __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    conn = db.get_db()
    cur = conn.cursor()

    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        cur.execute(
            'SELECT * FROM users WHERE id = (%s)', (user_id,)
        )
        g.user = cur.fetchone()


@bp.route("/login", methods=('GET', 'POST'))
def login():
    conn = db.get_db()
    cur = conn.cursor()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        cur.execute('SELECT * FROM users WHERE username = (%s)', (username,))
        user = cur.fetchone()

        if user is None:
            error = "Incorrect Credentials"
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect Credentials'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for("todos.index"))

    return render_template("login.html")


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

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

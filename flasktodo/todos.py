from flask import Blueprint, render_template, request, redirect, url_for

from . import db


bp = Blueprint("todos", __name__)

@bp.route("/")
def index():
    """View for home page which shows list of to-do items."""
    conn = db.get_db()
    cur = conn.cursor()

    cur.execute('SELECT * FROM todos')
    todos = cur.fetchall()
    cur.close()

    return render_template("index.html", todos=todos)


@bp.route("/<show>")
def filter(show):

    cur = db.get_db().cursor()

    if show == 'Completed':
        cur.execute('SELECT * FROM todos WHERE completed = TRUE')
        todos = cur.fetchall()
        cur.close()
        return render_template("index.html", todos=todos, filter=show)

    if show == 'Uncompleted':
        cur.execute('SELECT * FROM todos WHERE completed = FALSE')
        todos = cur.fetchall()
        cur.close()
        return render_template("index.html", todos=todos, filter=show)

    if show == 'All':
        cur.execute('SELECT * FROM todos')
        todos = cur.fetchall()
        cur.close()
        return render_template("index.html", todos=todos, filter=show)

@bp.route("/addtask", methods=('POST',))
def add_new_task():
    conn = db.get_db()
    cur = conn.cursor()

    if request.method == 'POST':
        newtask = request.form['newtask']

        cur.execute("INSERT INTO todos (description, completed, created_at) VALUES (%s, FALSE, NOW())",
                    (newtask,))
        conn.commit()

        return redirect(url_for('todos.index'))

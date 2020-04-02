
from flask import Blueprint, render_template, request, redirect, url_for, session, g

from . import db
from flasktodo.auth import login_required

from werkzeug.exceptions import abort

bp = Blueprint("todos", __name__)
#----------------------------------------------------------------------#
@bp.route("/", methods=('GET', 'POST'))
#@login_required
def index():
    """View for home page which shows list of to-do items."""
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM todos')
    todos = cur.fetchall()
    cur.close()

    #Filtering what shows
    show = filter(request.args.get('show'))
    show_title = request.args.get('show')

    if show:
        return render_template("index.html", todos=show, filter=show_title)

    return render_template("index.html", todos=todos, filter=show_title)
#----------------------------------------------------------------------#
def filter(show):
    """View for filtering todos"""
    cur = db.get_db().cursor()

    if show == 'Completed': #Shows todos where completed is TRUE
        cur.execute('SELECT * FROM todos WHERE completed = TRUE')
        todos = cur.fetchall()
        cur.close()
        return todos

    if show == 'Uncompleted': #Shows todos where completed is FALSE
        cur.execute('SELECT * FROM todos WHERE completed = FALSE')
        todos = cur.fetchall()
        cur.close()
        return todos
#----------------------------------------------------------------------#
@bp.route("/addtask", methods=('POST',))
#@login_required
def add_new_task():
    """View for adding todos"""
    conn = db.get_db()
    cur = conn.cursor()

    if request.method == 'POST':
        newtask = request.form['newtask'] #newtask is equal to new todo

        cur.execute("INSERT INTO todos (description, completed, created_at) VALUES (%s, FALSE, NOW())",
                    (newtask,)) #newtask is added as description with completed as FASLE and time NOW
        conn.commit()

        return redirect(url_for('todos.index'))
#----------------------------------------------------------------------#
@bp.route("/deletetask", methods=('POST',))
#@login_required
def delete_task():
    """View for deleting todos"""

    conn = db.get_db()
    cur = conn.cursor()

    if request.method == 'POST': #each delete button has the value of the description
        task_to_delete = request.form.get("task_to_delete") # task_to_delete = description

        cur.execute("DELETE FROM todos WHERE description = (%s)", (task_to_delete,))
        conn.commit()

        return redirect(url_for('todos.index'))
#----------------------------------------------------------------------#
@bp.route("/markcomplete", methods=('POST',))
#@login_required
def mark_complete():
    """View for marking todos complete"""

    conn = db.get_db()
    cur = conn.cursor()

    if request.method == 'POST':
        done = request.form.get("done") # done = a description of chosen todo
        cur.execute("UPDATE todos SET completed = TRUE WHERE description = (%s)",
                    (done,)) # the todo is set to complete where chose description
        conn.commit()

        return redirect(url_for('todos.index'))
#----------------------------------------------------------------------#


@bp.route("/<int:id>/edittask", methods=('GET', 'POST'))
#@login_required
def edit_task(id):
    """View for editing todos"""

    conn = db.get_db()
    cur = conn.cursor()

    cur.execute('SELECT * FROM todos WHERE id = (%s);', (id,))
    todo = cur.fetchone()

    if todo is None:
        abort(404, "Todo not found.")

    if request.method == 'POST':
        newdesc = request.form.get('newdesc')
        cur.execute("UPDATE todos SET description = (%s) WHERE id = (%s);", (newdesc, id,))
        conn.commit()

        return redirect(url_for('todos.index'))

    cur.close()
    return render_template("edit.html", todo=todo, id=id)

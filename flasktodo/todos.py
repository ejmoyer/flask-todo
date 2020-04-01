from flask import Blueprint, render_template, request, redirect, url_for

from . import db


bp = Blueprint("todos", __name__)
#----------------------------------------------------------------------#
@bp.route("/")
def index():
    """View for home page which shows list of to-do items."""

    conn = db.get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM todos')
    todos = cur.fetchall()
    cur.close()

    return render_template("index.html", todos=todos)
#----------------------------------------------------------------------#
@bp.route("/<show>")
def filter(show):
    """View for filtering todos"""

    cur = db.get_db().cursor()

    if show == 'Completed': #Shows todos where completed is TRUE
        cur.execute('SELECT * FROM todos WHERE completed = TRUE')
        todos = cur.fetchall()
        cur.close()
        return render_template("index.html", todos=todos, filter='Completed')

    if show == 'Uncompleted': #Shows todos where completed is FALSE
        cur.execute('SELECT * FROM todos WHERE completed = FALSE')
        todos = cur.fetchall()
        cur.close()
        return render_template("index.html", todos=todos, filter='Uncompleted')

    if show == 'All': #redirects to index to show all
        return redirect(url_for("todos.index"))
#----------------------------------------------------------------------#
@bp.route("/addtask", methods=('POST',))
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

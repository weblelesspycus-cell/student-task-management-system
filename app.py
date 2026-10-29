import os
import sqlite3
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash, abort

APP_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.environ.get("DATABASE_PATH", os.path.join(APP_DIR, "tasks.db"))

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-development-secret")


def get_db():
    """Open a SQLite connection and return rows as dictionary-like objects."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                due_date TEXT,
                priority TEXT NOT NULL DEFAULT 'Medium'
                    CHECK(priority IN ('Low', 'Medium', 'High')),
                status TEXT NOT NULL DEFAULT 'Pending'
                    CHECK(status IN ('Pending', 'In Progress', 'Completed')),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)


@app.route("/")
def index():
    status_filter = request.args.get("status", "All")
    search_term = request.args.get("q", "").strip()
    allowed_statuses = {"All", "Pending", "In Progress", "Completed"}
    if status_filter not in allowed_statuses:
        status_filter = "All"

    query = "SELECT * FROM tasks WHERE 1=1"
    params = []
    if status_filter != "All":
        query += " AND status = ?"
        params.append(status_filter)
    if search_term:
        query += " AND (title LIKE ? OR description LIKE ?)"
        params.extend([f"%{search_term}%", f"%{search_term}%"])
    query += """
        ORDER BY
            CASE status WHEN 'Pending' THEN 1 WHEN 'In Progress' THEN 2 ELSE 3 END,
            CASE priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END,
            CASE WHEN due_date IS NULL OR due_date = '' THEN 1 ELSE 0 END,
            due_date ASC, id DESC
    """

    with get_db() as db:
        tasks = db.execute(query, params).fetchall()
        totals = {
            "all": db.execute("SELECT COUNT(*) FROM tasks").fetchone()[0],
            "pending": db.execute("SELECT COUNT(*) FROM tasks WHERE status='Pending'").fetchone()[0],
            "progress": db.execute("SELECT COUNT(*) FROM tasks WHERE status='In Progress'").fetchone()[0],
            "completed": db.execute("SELECT COUNT(*) FROM tasks WHERE status='Completed'").fetchone()[0],
        }

    return render_template(
        "index.html", tasks=tasks, totals=totals,
        status_filter=status_filter, search_term=search_term,
        today=date.today().isoformat()
    )


@app.route("/tasks", methods=["POST"])
def create_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    due_date = request.form.get("due_date", "").strip()
    priority = request.form.get("priority", "Medium")
    status = request.form.get("status", "Pending")

    if not title:
        flash("Task title is required.", "error")
        return redirect(url_for("index"))
    if len(title) > 120:
        flash("Task title must be 120 characters or fewer.", "error")
        return redirect(url_for("index"))
    if priority not in {"Low", "Medium", "High"}:
        priority = "Medium"
    if status not in {"Pending", "In Progress", "Completed"}:
        status = "Pending"

    with get_db() as db:
        db.execute(
            "INSERT INTO tasks (title, description, due_date, priority, status) VALUES (?, ?, ?, ?, ?)",
            (title, description, due_date or None, priority, status)
        )
    flash("Task added successfully.", "success")
    return redirect(url_for("index"))


@app.route("/tasks/<int:task_id>/update", methods=["POST"])
def update_task(task_id):
    status = request.form.get("status", "Pending")
    if status not in {"Pending", "In Progress", "Completed"}:
        abort(400, "Invalid task status.")
    with get_db() as db:
        cursor = db.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))
        if cursor.rowcount == 0:
            abort(404)
    flash("Task status updated.", "success")
    return redirect(url_for("index"))


@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    with get_db() as db:
        cursor = db.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        if cursor.rowcount == 0:
            abort(404)
    flash("Task deleted.", "success")
    return redirect(url_for("index"))


@app.errorhandler(400)
def bad_request(error):
    return render_template("error.html", code=400, message=getattr(error, "description", "Bad request")), 400


@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", code=404, message="The requested task or page could not be found."), 404


init_db()

if __name__ == "__main__":
    # The host must be 0.0.0.0 for access through Docker port publishing.
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=False)

from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task = request.form.get("task")

        conn = sqlite3.connect("tasks.db")
        c = conn.cursor()
        c.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        conn.commit()
        conn.close()

    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()

    return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()

    if request.method == "POST":
        new_task = request.form.get("task")
        c.execute("UPDATE tasks SET task=? WHERE id=?", (new_task, id))
        conn.commit()
        conn.close()
        return redirect("/")

    c.execute("SELECT * FROM tasks WHERE id=?", (id,))
    task = c.fetchone()
    conn.close()

    return render_template("edit.html", task=task)


if __name__ == "__main__":
    app.run(debug=True)
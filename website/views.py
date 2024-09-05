from flask import Flask, Blueprint, render_template, request, redirect, url_for

from .models import Todo
from . import db

my_view = Blueprint("my_view", __name__)

@my_view . route("/")
def home():
    todo_list = Todo.query.all()
    message = request.args.get ('message', None)
    return render_template("index.html", todo_list =todo_list, message = message)

@my_view.route("/add", methods=[ "POST" ])
def add():
    try:
        task = request.form.get("task")
        new_todo = Todo(task=task)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for ("my_view.home"))
    except:
        # let the user know what went wrong
        # give a chance to try again
        message = "There was an error adding your task please try again"
        return redirect(url_for ("my_view.home", message = message))

@my_view.route("/update/<todo_id>", methods=[ "POST" ])

def update_task(todo_id):
    task = Todo.query.get(todo_id)
    task.complete = not task.complete
    db.session.commit()
    return redirect('/')


@my_view.route("/delete/<todo_id>", methods=[ "POST" ])
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for ("my_view.home"))

@my_view.route("/edit/<int:todo_id>", methods=["GET", "POST"])
def edit(todo_id):
    todo = Todo.query.get(todo_id)
    if request.method == "POST":
        new_task = request.form.get("task")
        if todo:
            todo.task = new_task
            db.session.commit()
            return redirect(url_for("my_view.home"))
    return render_template("edit.html", todo=todo)
from flask import Blueprint, render_template, redirect, url_for
from .models import Task
from .forms import TaskForm
from . import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@bp.route('/add', methods=['GET', 'POST'])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('add_task.html', form=form)

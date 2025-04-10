from flask import Blueprint, render_template, redirect, url_for, request
from app.models import Task
from app.forms import TaskForm
from datetime import date
from app.models import Quote
from app.external import fetch_and_store_quote
from app.app import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    search = request.args.get('search', '')
    sort_by = request.args.get('sort_by', '')
    order = request.args.get('order', '')
    page = request.args.get('page', 1, type=int)

    tasks_query = Task.query

    if search:
        tasks_query = tasks_query.filter(Task.title.contains(search))

    if not sort_by:
        sort_by = 'created_at'
    if not order:
        order = 'desc'

    sort_column = getattr(Task, sort_by, None)
    if sort_column is None:
        sort_column = Task.created_at

    if order == 'desc':
        sort_column = sort_column.desc()
    else:
        sort_column = sort_column.asc()

    tasks = tasks_query.order_by(sort_column).paginate(page=page, per_page=10, error_out=False)
    
    today_quote = Quote.query.filter(db.func.date(Quote.timestamp) == date.today()).first()

    if not today_quote:
        fetch_and_store_quote()
        today_quote = Quote.query.filter(db.func.date(Quote.timestamp) == date.today()).first()

    return render_template('index.html', tasks=tasks, quote=today_quote)
    

@main.route('/add', methods=['GET', 'POST'])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            is_done=form.is_done.data,
            priority=form.priority.data
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('add_task.html', form=form)

@main.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        form.populate_obj(task)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('edit_task.html', form=form, task=task)

@main.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('main.index'))

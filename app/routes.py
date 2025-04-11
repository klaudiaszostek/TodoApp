from datetime import datetime
from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
import pytz
from app.models import Task, User, Quote
from app.forms import LoginForm, TaskForm, RegisterForm
from app.external import fetch_and_store_quote
from app.app import db

main = Blueprint('main', __name__)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/')
def index():
    search = request.args.get('search', '')
    sort_by = request.args.get('sort_by', '')
    order = request.args.get('order', '')
    page = request.args.get('page', 1, type=int)

    # Creating query
    tasks_query = Task.query

    # If the user is logged in, filter by user_id
    if current_user.is_authenticated:
        tasks_query = tasks_query.filter_by(user_id=current_user.id)

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

    # Pagination
    tasks = tasks_query.order_by(sort_column).paginate(page=page, per_page=5, error_out=False)

    # Downloading quote for today
    today_date = datetime.now(pytz.timezone('Europe/Warsaw')).date()
    today_quote = Quote.query.filter(db.func.date(Quote.timestamp) == today_date).first()

    if not today_quote:
        fetch_and_store_quote()  # Download and save the quote if there is none for today
        today_quote = Quote.query.filter(db.func.date(Quote.timestamp) == today_date).first()
    
    # Returning the view with tasks and quote
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
            priority=form.priority.data,
            user_id=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        flash('Your task has been added!', 'success')
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

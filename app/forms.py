from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, TextAreaField, DateTimeField, IntegerField, PasswordField
from wtforms.validators import DataRequired, NumberRange

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    due_date = DateTimeField('Due Date', format='%Y-%m-%dT%H:%M', default=datetime.now) 
    is_done = BooleanField('Done')
    priority = IntegerField('Priority (1–5)', validators=[NumberRange(min=1, max=5)])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

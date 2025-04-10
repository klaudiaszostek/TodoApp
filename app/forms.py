from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, TextAreaField, DateTimeField, IntegerField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    due_date = DateTimeField('Termin', format='%Y-%m-%dT%H:%M', default=datetime.now) 
    is_done = BooleanField('Done')
    priority = IntegerField('Priority (1–10)')
    submit = SubmitField('Submit')

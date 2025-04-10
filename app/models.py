from app.app import db
from datetime import datetime
import pytz

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    due_date = db.Column(db.DateTime)
    is_done = db.Column(db.Boolean, default=False)
    priority = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/Warsaw')))

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    author = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=db.func.now())
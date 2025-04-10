from datetime import datetime
from app import db

class User(db.Model):
    """
    User model representing account information.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Note: Use hashed passwords in production.
    unit_preference = db.Column(db.String(10), default='metric')  # 'metric' or 'imperial'
    height = db.Column(db.Float)  # Stored in cm

    weight_entries = db.relationship('WeightEntry', backref='user', lazy=True)
    weight_goals = db.relationship('WeightGoal', backref='user', lazy=True)
    bmi_entries = db.relationship('BMIEntry', backref='user', lazy=True)

class WeightEntry(db.Model):
    """
    Model representing a weight entry.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    weight_kg = db.Column(db.Float, nullable=False)  # Internally stored as kg.
    date = db.Column(db.Date, default=datetime.utcnow)

class WeightGoal(db.Model):
    """
    Model representing a weight goal.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    goal_weight_kg = db.Column(db.Float, nullable=False)
    target_date = db.Column(db.Date, nullable=False)

class BMIEntry(db.Model):
    """
    Model representing a BMI calculation entry.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bmi_value = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(20))
    date = db.Column(db.Date, default=datetime.utcnow)

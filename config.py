import os

class Config:
    """
    Application configuration settings for WeightTracker.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-default-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://wtuser:Bl4hCr4p!@@localhost/weight_tracker')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.environ.get('DEBUG', False)

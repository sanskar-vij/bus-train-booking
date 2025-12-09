import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-change-me'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # sqlite database stored in instance/booking.db
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or                 'sqlite:///' + os.path.join(basedir, 'instance', 'booking.db')

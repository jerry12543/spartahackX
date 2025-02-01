""""loanminnow development config"""
import os


APPLICATION_ROOT = '/'

SECRET_KEY = 'spartahackx'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'db.sqlite')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

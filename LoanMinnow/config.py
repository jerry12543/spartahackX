""""loanminnow development config"""
import os
import pathlib


APPLICATION_ROOT = '/'

SECRET_KEY = 'spartahackx'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

LOANMINNOWROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = pathlib.Path(os.path.join(LOANMINNOWROOT, "var", "uploads"))
DB_PATH = pathlib.Path(os.path.join(LOANMINNOWROOT, "var", "loanminnow.db"))
SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
SQLALCHEMY_TRACK_MODIFICATIONS = False


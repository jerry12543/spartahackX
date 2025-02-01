import flask
from flask_sqlalchemy import SQLAlchemy
from loanminnow.api.routes import api_blueprint
from loanminnow.api.authtools import auth_blueprint
from loanminnow.api.search import search_blueprint
from flask_login import LoginManager
from flask_migrate import Migrate
from loanminnow.model import db, User

login_manager = LoginManager()

migrate = Migrate()

def create_app():
    """Flask application factory pattern."""
    app = flask.Flask(__name__)
    app.config.from_object('loanminnow.config')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    # redirects to /login if the user tries to access a protected route
    login_manager.login_view = 'auth.login'

    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(search_blueprint, url_prefix='/search')
    
    return app

@login_manager.user_loader
def load_user(user_id):
    """Loads a user by ID for Flask-Login."""    
    return User.query.get(int(user_id))# Initialize the application

app = create_app()

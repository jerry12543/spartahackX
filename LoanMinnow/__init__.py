import flask
import loanminnow.api
from loanminnow.api.routes import api_blueprint
from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy object; later bound to the app instance.
db = SQLAlchemy()

def create_app():
    app = flask.Flask(__name__)
    app.config.from_object('loanminnow.config')
    app.register_blueprint(api_blueprint, url_prefix='/api')

    db.init_app(app)
    with app.app_context():
        from loanminnow import models
        db.create_all()
    
    return app

app = create_app()
with app.app_context():
    db.create_all()

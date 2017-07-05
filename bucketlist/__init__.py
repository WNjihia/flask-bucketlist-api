from instance.config import app_config  # Load the views
from flask import Flask
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

# Initialize the app
app = Flask(__name__, instance_relative_config=True)

# initialize sql-alchemy
db = SQLAlchemy()


# Load the config file
def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from bucketlist.auth.views import auth_blueprint
    from bucketlist.api.views import api_blueprint

    # register Blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(api_blueprint)

    return app

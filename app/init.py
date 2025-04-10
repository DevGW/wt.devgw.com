from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Instantiate SQLAlchemy and Flask-Migrate.
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=None):
    """
    Application factory to create and configure the WeightTracker app.

    Args:
        config_class: The configuration class to load.

    Returns:
        Configured Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(config_class or 'config.Config')

    # Initialize extensions.
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints.
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

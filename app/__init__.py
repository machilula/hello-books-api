from flask import Flask
from .db import db, migrate
from .models import book, author
from .routes.book_routes import bp as book_bp
# I changed the author bp to author_bp and the tests are passing again
from .routes.author_routes import author_bp
import os

def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        # Merge `config` into the app's configuration
        # to override the app's default settings
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    app.register_blueprint(book_bp)
    app.register_blueprint(author_bp)

    return app


# the tests using the bp for books stopped passing after registering the authors bp
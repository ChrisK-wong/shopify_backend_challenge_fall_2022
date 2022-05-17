from flask import Flask, jsonify
from .models import *


def create_app():
    """
    Build flask app and initiate handlers and blueprints

    :return: flask app object
    """

    app = __create_app()
    __error_handlers(app)

    # route: /items
    from .inventory import items
    app.register_blueprint(items)

    # route: /shipments
    from .shipment import shipments
    app.register_blueprint(shipments)

    return app


def create_database():
    """
    Create database tables with flask app. This only needs to be ran once.

    :return: None
    """
    app = __create_app()
    with app.app_context():
        db.create_all()


def __create_app():
    """
    Helper function to create flask app with database

    :return: flask app object
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
    db.init_app(app)
    return app


def __error_handlers(app):
    """
    Create error handlers for flask app

    :param app: flask app object
    :return: None
    """
    @app.errorhandler(400)
    def handle_400_error(error):
        return jsonify({'error': 'Invalid request'}), 400

    @app.errorhandler(404)
    def handle_404_error(error):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(409)
    def handle_409_error(error):
        return jsonify({'error': 'Conflict has occurred'}), 409
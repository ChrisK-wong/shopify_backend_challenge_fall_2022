from flask import Flask, jsonify
from .models import *


def create_app():
    app = __create_app()
    __error_handlers(app)

    from .inventory import items
    app.register_blueprint(items)

    from .shipment import shipments
    app.register_blueprint(shipments)

    return app


def create_database():
    app = __create_app()
    with app.app_context():
        db.create_all()


def __create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
    db.init_app(app)
    return app


def __error_handlers(app):
    @app.errorhandler(400)
    def handle_400_error(error):
        return jsonify({'error': 'Invalid request'}), 400

    @app.errorhandler(404)
    def handle_404_error(error):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(409)
    def handle_409_error(error):
        return jsonify({'error': 'Conflict has occurred'}), 409
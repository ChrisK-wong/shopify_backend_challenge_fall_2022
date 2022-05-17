from flask import Blueprint, abort, request, jsonify
from .models import db, Inventory
from .util import view_item

items = Blueprint('api/items', __name__, url_prefix='/api/items')


@items.route('/', methods=['GET'])
@items.route('/<int:id>', methods=['GET'])
def read(id=''):
    """
    Get item(s) from database

    :param id: int
    :return: json
    """
    if id:
        # Try to get item from database
        item = Inventory.query.get_or_404(id)
        return jsonify(view_item(item))
    else:
        # Get all items from database
        items = Inventory.query.all()
        result = []
        for item in items:
            result.append(view_item(item))
        return jsonify(result)


@items.route('/', methods=['POST'])
def create():
    """
    Add new item to database

    Requires json {"name": str, "quantity": int}
    :return: json
    """
    # Get keys/values from json
    data = request.get_json()
    item_name = data.get('name')
    item_quantity = data.get('quantity')
    if not item_name:
        abort(400)
    if not item_quantity.isdigit() or int(item_quantity) < 0:
        abort(400)
    # Create item in database
    item = Inventory(name=item_name, quantity=int(item_quantity))
    db.session.add(item)
    db.session.commit()
    return jsonify(success=True)


@items.route('/<int:id>/update', methods=['PUT'])
def update(id):
    """
    Update data of item in database

    Requires json {"name": str, "quantity": int}
    :param id: int
    :return: json
    """
    # Get keys/values from json
    data = request.get_json()
    item_name = data.get('name')
    item_quantity = data.get('quantity')
    if not item_name:
        abort(400)
    if not item_quantity.isdigit() or int(item_quantity) < 0:
        abort(400)
    # Try to get item from database and update it
    item = Inventory.query.get_or_404(id)
    item.name = item_name
    item.quantity = item_quantity
    db.session.commit()
    return jsonify(success=True)


@items.route('/<int:id>/delete', methods=['DELETE'])
def delete(id):
    """
    Delete item from database

    :param id: int
    :return: json
    """
    # Try to get item from database and delete it
    item = Inventory.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify(success=True)

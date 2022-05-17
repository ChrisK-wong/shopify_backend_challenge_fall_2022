from flask import Blueprint, abort, request, jsonify
from .models import db, Inventory, Shipments, ShipmentItems
from .util import view_shipment

shipments = Blueprint('api/shipments', __name__, url_prefix='/api/shipments')


@shipments.route('/', methods=['GET'])
@shipments.route('/<int:id>', methods=['GET'])
def read(id=''):
    """
    Get shipment(s) from database

    :param id: int
    :return: json
    """
    if id:
        # Try to get shipment from database
        shipment = Shipments.query.get_or_404(id)
        return jsonify(view_shipment(shipment))

    else:
        # Get all shipments from database
        shipments = Shipments.query.all()
        result = []
        for s in shipments:
            result.append(view_shipment(s))
        return jsonify(result)


@shipments.route('/', methods=['POST'])
def create():
    """
    Add new shipment to database

    Requires json {"description": str, "address": str}
    :return: json
    """
    # Get keys/values from json
    data = request.get_json()
    ship_desc = data.get('description')
    ship_addr = data.get('address')
    if not (ship_desc and ship_addr):
        abort(400)
    # Create shipment in database
    ship_details = Shipments(description=ship_desc, address=ship_addr)
    db.session.add(ship_details)
    db.session.commit()
    return jsonify(success=True)


@shipments.route('/<int:id>/update', methods=['PUT'])
def update(id):
    """
    Update data of shipment in database

    Requires json {"description": str, "address": str}
    :param id: int
    :return: json
    """
    # Get keys/values from json
    data = request.get_json()
    ship_desc = data.get('description')
    ship_addr = data.get('address')
    if not (ship_desc and ship_addr):
        abort(400)
    # Try to get shipment from database and update it
    shipment = Shipments.query.get_or_404(id)
    shipment.description = ship_desc
    shipment.address = ship_addr
    db.session.commit()
    return jsonify(success=True)


@shipments.route('/<int:id>/delete', methods=['DELETE'])
def delete(id):
    """
    Delete shipment from database and adjust inventory accordingly

    :param id: int
    :return: json
    """
    # Try to get shipment from database and delete it
    shipment = Shipments.query.get_or_404(id)
    # Add back items to inventory
    for ship_items in shipment.items:
        item = Inventory.query.get(ship_items.item_id)
        item.quantity += ship_items.quantity
    db.session.delete(shipment)
    db.session.commit()
    return jsonify(success=True)


@shipments.route('/<int:ship_id>/add', methods=['POST'])
def add(ship_id):
    """
    Add an item to a shipment and adjust inventory accordingly

    Requires json {"item_id": int, "quantity": int}
    :param ship_id: int
    :return: json
    """
    # get keys/values from json
    data = request.get_json()
    item_id = data.get('item_id')
    item_quantity = data.get('quantity')
    if not item_id.isdigit():
        abort(400)
    if not item_quantity.isdigit() or int(item_quantity) < 1:
        abort(400)
    # Try to get shipment and item from database
    shipment = Shipments.query.get_or_404(ship_id)
    item = Inventory.query.get_or_404(item_id)
    # Check if enough of item in inventory
    if item.quantity < int(item_quantity):
        abort(409)
    item.quantity -= int(item_quantity)
    ship_item = ShipmentItems.query.filter_by(ship_id=ship_id, item_id=item_id).first()
    if ship_item:
        # Item already in shipment
        ship_item.quantity += int(item_quantity)
    else:
        # Add new item to shipment
        ship_item = ShipmentItems(quantity=int(item_quantity))
        ship_item.item = item
        shipment.items.append(ship_item)
    db.session.commit()
    return jsonify(success=True)


@shipments.route('/<int:ship_id>/<int:item_id>/remove', methods=['DELETE'])
def remove(ship_id, item_id):
    """
    Remove an item from a shipment and adjust inventory accordingly

    :param ship_id: int
    :param item_id: int
    :return: json
    """
    # Try to get shipment from database
    ship_item = ShipmentItems.query.filter_by(ship_id=ship_id, item_id=item_id).first()
    if ship_item:
        # Try to item from database and increment quantity from shipment
        item = Inventory.query.get_or_404(item_id)
        item.quantity += ship_item.quantity
        db.session.delete(ship_item)
        db.session.commit()
    return jsonify(success=True)

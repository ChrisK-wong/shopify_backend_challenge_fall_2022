from flask import Blueprint, abort, request, jsonify
from .models import db, Inventory, Shipments, ShipmentItems
from .util import view_shipment

shipments = Blueprint('api/shipments', __name__, url_prefix='/api/shipments')


@shipments.route('/', methods=['GET'])
@shipments.route('/<int:id>', methods=['GET'])
def read(id=''):
    if id:
        shipment = Shipments.query.get_or_404(id)
        return jsonify(view_shipment(shipment))

    else:
        shipments = Shipments.query.all()
        result = []
        for s in shipments:
            result.append(view_shipment(s))
        return jsonify(result)


@shipments.route('/', methods=['POST'])
def create():
    data = request.get_json()
    ship_desc = data.get('description')
    ship_addr = data.get('address')
    if not (ship_desc and ship_addr):
        abort(400)
    ship_details = Shipments(description=ship_desc, address=ship_addr)
    db.session.add(ship_details)
    db.session.commit()
    return jsonify(success=True)


@shipments.route('/<int:id>/update', methods=['PUT'])
def update(id):
    data = request.get_json()
    ship_desc = data.get('description')
    ship_addr = data.get('address')
    if not (ship_desc and ship_addr):
        abort(400)
    shipment = Shipments.query.get_or_404(id)
    shipment.description = ship_desc
    shipment.address = ship_addr
    db.session.commit()
    return jsonify(success=True)


@shipments.route('/<int:id>/delete', methods=['DELETE'])
def delete(id):
    shipment = Shipments.query.get_or_404(id)
    for ship_items in shipment.items:
        item = Inventory.query.get(ship_items.item_id)
        item.quantity += ship_items.quantity
    db.session.delete(shipment)
    db.session.commit()
    return jsonify(success=True)


@shipments.route('/<int:ship_id>/add', methods=['POST'])
def add(ship_id):
    data = request.get_json()
    try:
        item_id = int(data.get('item_id'))
        item_quantity = int(data.get('quantity'))
        if item_quantity < 1:
            abort(400)
    except (ValueError, TypeError):
        abort(400)
    shipment = Shipments.query.get_or_404(ship_id)
    item = Inventory.query.get_or_404(item_id)
    if item.quantity < item_quantity:
        abort(409)
    item.quantity -= item_quantity
    ship_item = ShipmentItems.query.filter_by(ship_id=ship_id, item_id=item_id).first()
    if ship_item:
        ship_item.quantity += item_quantity
    else:
        ship_item = ShipmentItems(quantity=item_quantity)
        ship_item.item = item
        shipment.items.append(ship_item)
    db.session.commit()
    return jsonify(success=True)


@shipments.route('/<int:ship_id>/<int:item_id>/remove', methods=['DELETE'])
def remove(ship_id, item_id):
    ship_item = ShipmentItems.query.filter_by(ship_id=ship_id, item_id=item_id).first()
    if ship_item:
        item = Inventory.query.get_or_404(item_id)
        item.quantity += ship_item.quantity
        db.session.delete(ship_item)
        db.session.commit()
    return jsonify(success=True)

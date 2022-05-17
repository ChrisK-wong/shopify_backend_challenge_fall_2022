from flask import Blueprint, abort, request, jsonify
from .models import db, Inventory
from .util import view_item

items = Blueprint('api/items', __name__, url_prefix='/api/items')


@items.route('/', methods=['GET'])
@items.route('/<int:id>', methods=['GET'])
def read(id=''):
    if id:
        item = Inventory.query.get_or_404(id)
        return jsonify(view_item(item))
    else:
        items = Inventory.query.all()
        result = []
        for item in items:
            result.append(view_item(item))
        return jsonify(result)


@items.route('/', methods=['POST'])
def create():
    data = request.get_json()
    item_name = data.get('name')
    if not item_name:
        abort(400)
    try:
        item_quantity = int(data.get('quantity'))
        if item_quantity < 0:
            abort(400)
    except (ValueError, TypeError):
        abort(400)
    item = Inventory(name=item_name, quantity=item_quantity)
    db.session.add(item)
    db.session.commit()
    return jsonify(success=True)


@items.route('/<int:id>/update', methods=['PUT'])
def update(id):
    data = request.get_json()
    item_name = data.get('name')
    if not item_name:
        abort(400)
    try:
        item_quantity = int(data.get('quantity'))
        if item_quantity < 0:
            abort(400)
    except (ValueError, TypeError):
        abort(400)
    item = Inventory.query.get_or_404(id)
    item.name = item_name
    item.quantity = item_quantity
    db.session.commit()
    return jsonify(success=True)


@items.route('/<int:id>/delete', methods=['DELETE'])
def delete(id):
    item = Inventory.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify(success=True)

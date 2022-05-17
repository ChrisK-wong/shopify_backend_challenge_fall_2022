from flask import Blueprint, request, render_template, url_for, redirect
import requests

web = Blueprint('web', __name__, url_prefix='/web', template_folder='templates', static_folder='static')


def redir(response):
    return redirect(url_for('web.index', response=f'{response} {response.json()}'))


@web.route('/', methods=['GET'])
def index():
    response = requests.get(url_for('api/items.read', _external=True))
    items = response.json()
    response = requests.get(url_for('api/shipments.read', _external=True))
    shipments = response.json()
    response = request.args.get('response', '')
    return render_template('index.html', inventory=items, shipments=shipments, response=response)


@web.route('/', methods=['POST'])
def create():
    item_name = request.form.get('name', '')
    item_quantity = request.form.get('quantity', 0)
    data = {
        'name': item_name,
        'quantity': item_quantity
    }
    response = requests.post(url_for('api/items.create', _external=True), json=data)
    return redir(response)


@web.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'GET':
        response = requests.get(url_for('api/items.read', id=id, _external=True))
        item = response.json()
        return render_template('edit.html', item=item)
    else:
        item_name = request.form.get('name', '')
        item_quantity = request.form.get('quantity', 0)
        data = {
            'name': item_name,
            'quantity': item_quantity
        }
        response = requests.put(url_for('api/items.update', id=id, _external=True), json=data)
        return redir(response)


@web.route('<int:id>/delete', methods=['GET'])
def delete(id):
    response = requests.delete(url_for('api/items.delete', id=id, _external=True))
    return redir(response)


@web.route('shipment', methods=['POST'])
def create_shipment():
    ship_desc = request.form.get('description')
    ship_addr = request.form.get('address')
    data = {
        'description': ship_desc,
        'address': ship_addr
    }
    response = requests.post(url_for('api/shipments.create', _external=True), json=data)
    return redir(response)


@web.route('shipment/<int:id>/edit', methods=['GET', 'POST'])
def edit_shipment(id):
    if request.method == 'GET':
        response = requests.get(url_for('api/shipments.read', id=id, _external=True))
        shipment = response.json()
        return render_template('edit_shipment.html', shipment=shipment)
    else:
        ship_desc = request.form.get('description')
        ship_addr = request.form.get('address')
        data = {
            'description': ship_desc,
            'address': ship_addr
        }
        response = requests.put(url_for('api/shipments.update', id=id, _external=True), json=data)
        return redir(response)


@web.route('shipment/<int:id>/delete', methods=['GET'])
def delete_shipment(id):
    response = requests.delete(url_for('api/shipments.delete', id=id, _external=True))
    return redir(response)


@web.route('shipment/<int:id>/add', methods=['POST'])
def add_shipment_item(id):
    item_id = request.form.get('item_id')
    quantity = request.form.get('quantity')
    data = {
        'item_id': item_id,
        'quantity': quantity
    }
    response = requests.post(url_for('api/shipments.add', ship_id=id, _external=True), json=data)
    return redir(response)


@web.route('shipment/<int:ship_id>/<int:item_id>/remove', methods=['GET'])
def remove_shipment_item(ship_id, item_id):
    response = requests.delete(url_for('api/shipments.remove', ship_id=ship_id, item_id=item_id, _external=True))
    return redir(response)
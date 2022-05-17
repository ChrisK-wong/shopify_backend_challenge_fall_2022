def view_item(item):
    """
    :param item: query objet
    :return: dict
    """
    data = {
        'id': item.id,
        'name': item.name,
        'quantity': item.quantity
    }
    return data


def view_shipment(shipment):
    """
    :param shipment: query object
    :return: dict
    """
    items = []
    for ship_item in shipment.items:
        item_data = {
            'item_id': ship_item.item_id,
            'name': ship_item.item.name,
            'quantity': ship_item.quantity
        }
        items.append(item_data)
    data = {
        'id': shipment.id,
        'description': shipment.description,
        'address': shipment.address,
        'items': items
    }
    return data
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Inventory(db.Model):
    """
    This model defines the Inventory table where each row represents a unique item
    """
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    shipments = db.relationship('ShipmentItems', back_populates='item', cascade='all, delete')

    def __repr__(self):
        return f'<Inventory {self.id}>'


class Shipments(db.Model):
    """
    This model defines the Shipments table where each row represents a unique shipment
    """
    __tablename__ = 'shipments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    items = db.relationship('ShipmentItems', back_populates='ship')

    def __repr__(self):
        return f'<Shipment {self.id}>'


class ShipmentItems(db.Model):
    """
    This is an association model for many-to-many relationship between shipments and inventory items.
    Additional key "quantity" is use to keep track of an item amount is inside the shipment.
    """
    __tablename__ = 'shipment_items'
    id = db.Column(db.Integer, primary_key=True)
    ship_id = db.Column(db.Integer, db.ForeignKey('shipments.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('inventory.id'))
    quantity = db.Column(db.Integer, nullable=False)
    ship = db.relationship("Shipments", back_populates='items')
    item = db.relationship("Inventory", back_populates='shipments')
    __table_args__ = (db.UniqueConstraint('ship_id', 'item_id'),)

    def __repr__(self):
        return f'<ShipmentItems {self.id}>'
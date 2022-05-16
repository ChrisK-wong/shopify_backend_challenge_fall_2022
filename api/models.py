from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ShipmentItems(db.Model):
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


class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    shipments = db.relationship('ShipmentItems', back_populates='item', cascade='all, delete')

    def __repr__(self):
        return f'<Inventory {self.id}>'


class Shipments(db.Model):
    __tablename__ = 'shipments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    items = db.relationship('ShipmentItems', back_populates='ship')

    def __repr__(self):
        return f'<Shipment {self.id}>'

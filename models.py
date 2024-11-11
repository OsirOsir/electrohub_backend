from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import MetaData, func
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

# Initialize SQLAlchemy and Bcrypt
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


# Item Model
item_special_categories = db.Table(
        'item_special_categories',
        db.Column('item_id', db.Integer, db.ForeignKey('items.id'), primary_key=True),
        db.Column('special_category_id', db.Integer, db.ForeignKey('special_categories.id'), primary_key=True)
    )

class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String, nullable=False, unique=True)
    item_features = db.Column(db.String, nullable=False)
    item_price = db.Column(db.Integer, nullable=False)
    item_prev_price = db.Column(db.Integer)
    item_image_url = db.Column(db.Text, nullable=False)
    item_category = db.Column(db.String, nullable=False)
    items_in_stock = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    modified_at = db.Column(db.DateTime, default=func.now(), default=func.now())
    
    # Many-to-many relationship with SpecialCategory
    special_categories = db.relationship(
        'SpecialCategory',
        secondary=item_special_categories,
        backref=db.backref('items', lazy=True)
    )
    
    # Check if the item is in stock
    def is_in_stock(self):
        return self.items_in_stock > 0

# SpecialCategory Model
class SpecialCategory(db.Model, SerializerMixin):
    __tablename__ = "special_categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
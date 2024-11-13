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

#User Model
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    serialize_rules = ('-reviews.user',)
    
    id = id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    
    reviews = db.relationship('Review', back_populates="user", cascade='all, delete-orphan')
    
# Item Model
item_special_categories = db.Table(
        'item_special_categories',
        db.Column('item_id', db.Integer, db.ForeignKey('items.id'), primary_key=True),
        db.Column('special_category_id', db.Integer, db.ForeignKey('special_categories.id'), primary_key=True)
    )

class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'
    
    serialize_rules = ('-reviews.item', '-reviews.user',)
    
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String, nullable=False, unique=True)
    item_features = db.Column(db.String, nullable=False)
    item_price = db.Column(db.Integer, nullable=False)
    item_prev_price = db.Column(db.Integer)
    item_image_url = db.Column(db.Text, nullable=False)
    item_category = db.Column(db.String, nullable=False)
    items_in_stock = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    modified_at = db.Column(db.DateTime, onupdate=func.now())
    
    reviews = db.relationship('Review', back_populates="item", cascade='all, delete-orphan')
    
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
    
    serialize_rules = ('-items',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    
    
class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"
    
    serialize_rules = ('-item.reviews', '-user.reviews',)
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    review_message = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=func.now())
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    item = db.relationship('Item', back_populates="reviews")
    user = db.relationship('User', back_populates="reviews")
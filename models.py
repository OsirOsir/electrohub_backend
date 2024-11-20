from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import MetaData, func
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
from flask_bcrypt import Bcrypt

# Initialize SQLAlchemy and Bcrypt
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)
from flask_login import UserMixin

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    serialize_rules = ('-reviews.user',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    _password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default='user')
    is_active = db.Column(db.Boolean, default=True)

    
    items = db.relationship('Item', back_populates='user', lazy=True, cascade="all, delete-orphan")

    cart_items = db.relationship('Cart', back_populates='user', lazy=True, cascade="all, delete-orphan")

    reviews = db.relationship('Review', back_populates="user", cascade='all, delete-orphan')

    @hybrid_property
    def password(self):
        raise AttributeError('Password is not readable!')

    @password.setter
    def password(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'<User(name={self.username}, role={self.role}, is_active={self.is_active})>'

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
    item_features = db.Column(JSONB, nullable=False)
    item_price = db.Column(db.Integer, nullable=False)
    item_prev_price = db.Column(db.Integer)
    item_image_url = db.Column(db.Text, nullable=False)
    item_category = db.Column(db.String, nullable=False)
    items_in_stock = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    modified_at = db.Column(db.DateTime, onupdate=func.now())

    cart_items = db.relationship('Cart', back_populates='item', lazy=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # user = db.relationship('User', back_populates='items')
    user = db.relationship('User', back_populates='items')  # Assuming a relationship with User model

    reviews = db.relationship('Review', back_populates="item", cascade='all, delete-orphan')
    
    # Many-to-many relationship with SpecialCategory
    special_categories = db.relationship(
        'SpecialCategory',
        secondary=item_special_categories,
        backref=db.backref('items', lazy=True)
    )
    
    def __repr__(self):
        return f'<Item: {self.item_name}, Features: {self.item_features}, Price: {self.item_price}, Category: {self.item_category}'
    
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


    
# Cart Model
class Cart(db.Model, SerializerMixin):
    __tablename__ = 'carts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=func.now())
    modified_at = db.Column(db.DateTime, onupdate=func.now())

    # Relationships
    user = db.relationship('User', back_populates='cart_items')
    item = db.relationship('Item', back_populates='cart_items')

    def __repr__(self):
        return f'<Cart(user_id={self.user_id}, items_id={self.item_id}, quantity={self.quantity})>'






# class Product(db.Model):
#     __tablename__ = 'products'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(150), nullable=False)
#     description = db.Column(db.Text, nullable=True)
#     price = db.Column(db.Float, nullable=False)
#     item_availability = db.Column(db.Integer, nullable=False, default=0)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    
    
#     def __repr__(self):
#         return f'<Product(name={self.name}, price=${self.price}, item_availability={self.item_availability})>'

#User Model
# class User(db.Model, SerializerMixin):
#     __tablename__ = 'users'
    
    
    
#     id = id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String, nullable=False, unique=True)
#     role = db.Column(db.String(50), default='user')
#     is_active = db.Column(db.Boolean, default=True)
    
    

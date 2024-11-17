from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()

# Many-to-many relationship between Item and SpecialCategory
item_special_categories = db.Table(
    'item_special_categories',
    db.Column('item_id', db.Integer, db.ForeignKey('items.id'), primary_key=True),
    db.Column('special_category_id', db.Integer, db.ForeignKey('special_categories.id'), primary_key=True)
)

# User Model
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    _password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default='user')  # Default role is 'user'
    is_active = db.Column(db.Boolean, default=True)

    # Relationship to items owned by the user
    items = db.relationship('Item', back_populates='owner', lazy=True, cascade="all, delete-orphan")

    # Relationship to cart items
    cart_items = db.relationship('Cart', back_populates='user', lazy=True, cascade="all, delete-orphan")

    # Password property to store the hash and avoid exposing password
    @hybrid_property
    def password(self):
        raise AttributeError('Password is not readable!')

    @password.setter
    def password(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def authenticate(self, password):
        """Authenticate the user with the given password."""
        return bcrypt.check_password_hash(self._password_hash, password)

    def is_admin(self):
        """Return True if the user is an admin."""
        return self.role == 'admin'

    def __repr__(self):
        return f'<User(name={self.name}, role={self.role}, is_active={self.is_active})>'

# Item Model (formerly Product)
class Item(db.Model):
    __tablename__ = 'items'
    
    serialize_rules = ('-reviews.item', '-reviews.user',)
    
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(150), nullable=False, unique=True)
    item_features = db.Column(db.JSON, nullable=False)
    item_price = db.Column(db.Integer, nullable=False)
    item_prev_price = db.Column(db.Integer)
    item_image_url = db.Column(db.Text, nullable=False)
    item_category = db.Column(db.String, nullable=False)
    items_in_stock = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    modified_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    # Relationships
    reviews = db.relationship('Review', back_populates="item", cascade='all, delete-orphan')
    special_categories = db.relationship(
        'SpecialCategory',
        secondary=item_special_categories,
        backref=db.backref('items', lazy=True)
    )
    owner = db.relationship('User', back_populates='items')

    def __repr__(self):
        return f'<Item(name={self.item_name}, price={self.item_price}, in_stock={self.items_in_stock})>'

    # Check if the item is in stock
    def is_in_stock(self):
        return self.items_in_stock > 0

# SpecialCategory Model
class SpecialCategory(db.Model):
    __tablename__ = 'special_categories'
    
    serialize_rules = ('-items',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<SpecialCategory(name={self.name})>'

# Review Model
class Review(db.Model):
    __tablename__ = 'reviews'
    
    serialize_rules = ('-item.reviews', '-user.reviews',)

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    review_message = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=db.func.now())
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    item = db.relationship('Item', back_populates="reviews")
    user = db.relationship('User', back_populates="reviews")

    def __repr__(self):
        return f'<Review(rating={self.rating}, user={self.user.name}, item={self.item.item_name})>'

# Cart Model
class Cart(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    # Relationships
    item = db.relationship('Item', back_populates='cart_items')
    user = db.relationship('User', back_populates='cart_items')

    def __repr__(self):
        return f'<Cart(user_id={self.user_id}, item_id={self.item_id}, quantity={self.quantity})>'

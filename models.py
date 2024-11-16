from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    _password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default='user')
    is_active = db.Column(db.Boolean, default=True)

    products = db.relationship('Product', backref='owner', lazy=True, cascade="all, delete-orphan")

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
        return f'<User(name={self.name}, role={self.role}, is_active={self.is_active})>'

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    item_availability = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Product(name={self.name}, price=${self.price}, item_availability={self.item_availability})>'
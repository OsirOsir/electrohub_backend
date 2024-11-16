from flask import Flask, jsonify, request
from models import db, User, Product
from flask_migrate import Migrate
from serializer import user_serializer, product_serializer
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from flask_restful import Api
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://groupthree:group3@localhost/electrohub_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'

db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
api = Api(app)
CORS(app)

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Admin check decorator
def admin_required(f):
    """Decorator to ensure the current user is an admin."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return "<h1>Welcome to ElectroHub</h1>"

# Handle users (GET and POST)
@app.route('/api/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([user_serializer(user) for user in users]), 200

    elif request.method == 'POST':
        data = request.json
        required_fields = ['name', 'email', 'password']

        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Name, email, and password are required'}), 400

        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'User with this email already exists'}), 400

        try:
            role = data.get('role', 'user')
            new_user = User(
                name=data['name'],
                email=data['email'],
                role=role
            )
            new_user.password = data['password']  
            db.session.add(new_user)
            db.session.commit()

            return jsonify(user_serializer(new_user)), 201

        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Database integrity error occurred'}), 500

# User login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data.get('email')).first()

    if user and user.is_active and user.authenticate(data.get('password')):
        login_user(user)
        return jsonify({'message': 'Login successful', 'user': user_serializer(user)}), 200
    return jsonify({'error': 'Invalid email or password'}), 401

# User logout
@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

# User profile
@app.route('/api/profile', methods=['GET'])
@login_required
def profile():
    return jsonify(user_serializer(current_user)), 200

# Delete account (user self-deletion)
@app.route('/api/users/delete', methods=['DELETE'])
@login_required
def delete_account():
    try:
        db.session.delete(current_user)
        db.session.commit()
        logout_user()
        return jsonify({'message': 'Account deleted successfully'}), 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Admin routes for managing products
@app.route('/api/admin/products', methods=['POST'])
@login_required
@admin_required
def add_product():
    data = request.json

    if 'name' not in data or 'price' not in data or 'user_id' not in data:
        return jsonify({'error': 'Name, price, and user_id are required'}), 400

    try:
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404

        new_product = Product(
            name=data['name'],
            description=data.get('description', ''),
            price=data['price'],
            item_availability=data.get('item_availability', 0),
            user_id=data['user_id']
        )
        db.session.add(new_product)
        db.session.commit()

        return jsonify(product_serializer(new_product)), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Get all products
@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product_serializer(product) for product in products]), 200

# Get user by ID
@app.route('/api/users/<int:id>', methods=['GET'])
@login_required
def get_user_by_id(id):
    user = User.query.get(id)
    if user:
        return jsonify(user_serializer(user)), 200
    return jsonify({'error': 'User not found'}), 404

# Admin delete user
@app.route('/api/users/<int:id>', methods=['DELETE'])
@login_required
@admin_required
def delete_user(id):
    user = User.query.get(id)
    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': f'User {id} deleted successfully.'}), 204
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5555)
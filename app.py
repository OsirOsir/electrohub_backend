import os
from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, jsonify, request, render_template, make_response, session
from models import db, User, Cart, Review, Item, SpecialCategory
from flask_migrate import Migrate
from serializer import user_serializer, item_serializer
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from flask_restful import Api, Resource
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps
from flask_cors import CORS


app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://groupthree:sfb31oTxBAToN04gFlsyk6X2ERbCp2oD@dpg-csvggau8ii6s73esk4ng-a.oregon-postgres.render.com/electrohub_db_5djp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'

#
SWAGGER_URL = '/swagger'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "electrohub_api"
    },
   
)

app.register_blueprint(swaggerui_blueprint, url_prefix = SWAGGER_URL)

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
api = Api(app)
CORS(app, supports_credentials=True)

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
        required_fields = ['username', 'email', 'password']

        if not all(field in data for field in required_fields):
            return jsonify({'error': 'User name, email, and password are required'}), 400

        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'User with this email already exists'}), 400

        try:
            role = data.get('role', 'user')
            new_user = User(
                username=data['username'],
                email=data['email'],
                role=role
            )
            new_user.password = data['password']
            db.session.add(new_user)
            db.session.commit()
            session['user_id']= new_user.id

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
        session['user_id']= user.id
        return jsonify({'message': 'Login successful', 'user': user_serializer(user)}), 200
    return jsonify({'error': 'Invalid email or password'}), 401

# User logout
@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)

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

# Get user by ID
@app.route('/api/users/<int:id>', methods=['GET'])
@login_required
def get_user_by_id(id):
    user = User.query.get(id)
    if user:
        return jsonify(user_serializer(user)), 200
    return jsonify({'error': 'User not found'}), 404

# Update user profile
@app.route('/api/users/update', methods=['PATCH'])
@login_required
def update_user():
    data = request.json

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    updated_name = data.get('name')
    updated_password = data.get('password')

    if not updated_name and not updated_password:
        return jsonify({'error': 'No name or password provided to update'}), 400

    try:
        if updated_name:
            current_user.name = updated_name

        if updated_password:
            hashed_password = bcrypt.generate_password_hash(updated_password).decode('utf-8')
            current_user.password = hashed_password

        db.session.commit()
        return jsonify({'message': 'Profile updated successfully', 'user': user_serializer(current_user)}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

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

# View cart
@app.route('/api/cart', methods=['GET'])
@login_required
def view_cart():
    # Fetch cart items for the current user
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    print(f"Found {len(cart_items)} cart items for user {current_user.id}")

    if not cart_items:
        return jsonify({'message': 'Your cart is empty.'}), 200

    cart_data = []
    for item in cart_items:
        print(f"Item: {item}, Item: {item.item}")  
        cart_data.append({
            'item': item_serializer(item.item),
            'quantity': item.quantity
        })

    return jsonify({'cart': cart_data}), 200


# Add item to cart
@app.route('/api/cart', methods=['POST'])
@login_required
def add_to_cart():
    data = request.json
    item_id = data.get('item_id')
    quantity = data.get('quantity', 1)

    item = Item.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    cart_item = Cart.query.filter_by(user_id=current_user.id, item_id=item_id).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = Cart(user_id=current_user.id, item_id=item_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    return jsonify({'message': 'Item added to cart successfully'}), 201

# Remove item from cart
@app.route('/api/cart/<int:item_id>', methods=['DELETE'])
@login_required
def remove_from_cart(item_id):
    cart_item = Cart.query.filter_by(user_id=current_user.id, item_id=item_id).first()
    if not cart_item:
        return jsonify({'error': 'Item not in cart'}), 404

    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'message': 'Item removed from cart'}), 204

# Update cart quantity
@app.route('/api/cart/<int:item_id>', methods=['PATCH'])
@login_required
def update_cart_quantity(item_id):
    data = request.json
    quantity = data.get('quantity')

    if not quantity or quantity <= 0:
        return jsonify({'error': 'Invalid quantity'}), 400

    cart_item = Cart.query.filter_by(user_id=current_user.id, item_id=item_id).first()
    if not cart_item:
        return jsonify({'error': 'Item not in cart'}), 404

    cart_item.quantity = quantity
    db.session.commit()
    return jsonify({'message': 'Cart updated successfully'}), 200



@app.route("/api/item/<int:item_id>/add_special_category", methods=["POST"])
def add_special_category_to_item(item_id):
    
    special_category_name = request.json["special_category_name"]
    
    item = Item.query.get(item_id)
    special_category = SpecialCategory.query.filter_by(name=special_category_name).first()
    
    if not item:
        return jsonify({"message": f"Item ID {item_id} not found."}), 404

    if not special_category:
        return jsonify({"message": f"Special Category '{special_category_name}' not found."}), 404

    if special_category in item.special_categories:
        return jsonify({"message": f"Item Id {item.id} is already in special category {special_category_name}."}), 200
    
    item.special_categories.append(special_category)
    db.session.commit()
    
    return jsonify({"message": f"Item id {item.id} {item.item_name} added to special Category {special_category_name}."}), 200
    
    
@app.route("/api/item/<int:item_id>/remove_special_category", methods=["DELETE"])
def remove_special_category_from_item(item_id):
    try:
        data = request.json
        if not data or "special_category_name" not in data:
            return jsonify({"message": "Error: Missing special_category_name in request body"}), 400

        special_category_name = data["special_category_name"]
        item = Item.query.get(item_id)
        special_category = SpecialCategory.query.filter_by(name=special_category_name).first()
    
        special_category_name = request.json["special_category_name"]
    
        item = Item.query.get(item_id)
        special_category = SpecialCategory.query.filter_by(name=special_category_name).first()

        if not item:
            return jsonify({"message": f"Item ID {item_id} not found."}), 404

        if not special_category:
            return jsonify({"message": f"Special Category '{special_category_name}' not found."}), 404

        if special_category not in item.special_categories:
            return jsonify({"message": f"Item Id {item.id} is not in special category {special_category_name}."}), 200
        
        item.special_categories.remove(special_category)
        db.session.commit()
        
        return jsonify({"message": f"Item id {item.id} {item.item_name} removed from special Category {special_category_name}."}), 200

    except Exception as e:
        return jsonify({"message": f"An unexpected error occurred: {str(e)}"}), 500
    
# Check items available for a specific item
@app.route("/api/item/<int:item_id>/items_in_stock", methods=["GET"])
def items_in_stock_for_items(item_id):
    
    try:
        item = Item.query.get(item_id)
        
        if not item:
            return jsonify({"message": "Item not found"}), 404
        
        return jsonify({"item_name": item.item_name, "items_in_stock": item.items_in_stock}), 200
    except Exception as e:
        return jsonify({"message": "An error occured while retrieving item data"}), 500

class CrudItems(Resource):
    def get(self):
        items_list = [item.to_dict() for item in Item.query.all()]
        
        if not items_list:
            response = make_response({"message": "No items available"}, 404,)
            return response
        
        response = make_response(items_list, 200,)
        return response
    
    #Add 'Create Item button' in the frontend
    #Create, Update, Delete only for Admin and when logged in
    def post(self):
        #Add constraints and validations to the fields when POSTing new review, all the required fields should be filled and descriptive messages in case of errors
        if 'user_id' not in session:
            return {'error': 'Unauthorized: Please log in first'}, 401
        
        user = User.query.filter_by(id=session['user_id']).first()
        
        if not user or user.role != 'Admin':
            return {'error': 'Forbidden: Only admins can perform this action'}, 403
        
        try:
            item_name = request.json['item_name']
            item_features = request.json['item_features']
            item_price = request.json['item_price']
            item_image_url = request.json['item_image_url']
            item_category = request.json['item_category']
            items_in_stock = request.json['items_in_stock']

            new_item = Item(
                item_name=item_name,
                item_features=item_features,
                item_price=item_price,
                item_image_url=item_image_url,
                item_category=item_category,
                items_in_stock=items_in_stock
            )

            db.session.add(new_item)
            db.session.commit()

            response_data = {
                'id': new_item.id,
                'item_name': new_item.item_name,
                'item_features': new_item.item_features,
                'item_price': new_item.item_price,
                'item_image_url': new_item.item_image_url,
                'item_category': new_item.item_category,
                'items_in_stock': new_item.items_in_stock
            }

            return make_response(jsonify(response_data), 201)

        except KeyError as e:
            return {"message": f"Missing required field: {str(e)}"}, 400

        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500
    
api.add_resource(CrudItems, '/api/items', endpoint="crudItems")


class CrudItemsById(Resource):
    #Add constraints and validations to the fields when PATCHing new review, all the required fields should be filled and descriptive messages in case of errors
    def patch(self, item_id):

        if 'user_id' not in session:
            return {'error': 'Unauthorized: Please log in first'}, 401
        
        user = User.query.filter_by(id=session['user_id']).first()
        
        if not user or user.role != 'Admin':
            return {'error': 'Forbidden: Only admins can perform this action'}, 403
        
        item = Item.query.filter(Item.id == item_id).first()
        
        if not item:
            response_dict = {"message": f"Item id {item_id} not found"}
            return make_response(response_dict, 404)
        
        for attr in request.json:
            if hasattr(item, attr):
                setattr(item, attr, request.json[attr])
                
        db.session.add(item)
        db.session.commit()
        
        response_dict = item.to_dict()
        
        return make_response(jsonify(response_dict), 200)
    
    def delete(self, item_id):
        if 'user_id' not in session:
            return {'error': 'Unauthorized: Please log in first'}, 401
        
        user = User.query.filter_by(id=session['user_id']).first()
        
        if not user or user.role != 'Admin':
            return {'error': 'Forbidden: Only admins can perform this action'}, 403
        
        item = Item.query.filter(Item.id == item_id).first()
        
        if not item:
            response_dict = {"message": f"Item id {item_id} not found"}
            return make_response(response_dict, 404)
        
        #Ask if they are sure that they would like to delete the item
        db.session.delete(item)
        db.session.commit()
        
        response_dict = {"message": f"Item id {item.id} {item.item_name} has been deleted successfully"}
        
        return make_response(response_dict, 200)
    
api.add_resource(CrudItemsById, '/api/items/item_id/<int:item_id>', endpoint="crudItemsById")


@app.route('/api/item_details/item_id/<int:item_id>', methods=["GET"])
def get_item_details(item_id):
    
    item = Item.query.filter_by(id=item_id).first()
    
    if not item:
        return jsonify({"message": f"Item id {item_id} not found"}), 404
    
    response = make_response(item.to_dict(), 200,)
    return response


@app.route('/api/items/reviews', methods=['GET'])
def get_all_reviews():
    
    reviews_list = [review.to_dict() for review in Review.query.all()]
    
    if not reviews_list:
        response = make_response({"message": "No reviews available"}, 404,)
        return response
    
    response = make_response(reviews_list, 200,)
    return response


class ItemReviewsById(Resource):
    def get(self, item_id):
        reviews_list = [review.to_dict() for review in Review.query.filter_by(item_id=item_id).all()]
        
        if not reviews_list:
            response = make_response({"message": f"Item id {item_id} has no reviews"}, 404)
            return response
            
        response = make_response(reviews_list, 200)
        return response
    

    def post(self, item_id):
        
        if 'user_id' not in session:
            return {'error': 'Unauthorized'}, 401
        
        try:
            rating = request.json['rating']
            review_message = request.json['review_message']
            user_id = session['user_id']
            
            
            new_review = Review(rating=rating, review_message=review_message, item_id=item_id, user_id=user_id)
            
            db.session.add(new_review)
            db.session.commit()
            
            response_data = {
                'id': new_review.id,
                'rating': new_review.rating,
                'review_message': new_review.review_message,
                'item_id': new_review.item_id,
                'user_id': new_review.user_id
            }
            
            return make_response(jsonify(response_data), 201)
            
        except KeyError as e:
            return {"message": f"Missing required field: {str(e)}"}, 400

        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500
            
api.add_resource(ItemReviewsById, '/api/item_id/<int:item_id>/reviews', endpoint="itemReviewsById")
    
class ModifyItemReviewById(Resource):
    
    def patch(self, review_id):
        
        # Also that the user.id matches the user.id of the owner of the review
        if 'user_id' not in session:
            return {'error': 'Unauthorized'}, 401
        
        review = Review.query.filter(Review.id == review_id).first()
        
        if not review:
            return make_response({"message": f"Review id {review_id} not found"})
        
        if review.user_id != session['user_id']:
            return {'error': 'Forbidden: You can only edit your own reviews'}, 403
        
        for attr in request.json:
            if hasattr(review, attr):
                setattr(review, attr, request.json[attr])
                
        db.session.add(review)
        db.session.commit()
        
        return make_response(jsonify(review.to_dict()), 200)
    
    
    def delete(self, review_id):
        
        # Also that the user.id matches the user.id of the owner of the review
        if 'user_id' not in session:
            return {'error': 'Unauthorized'}, 401
        
        review = Review.query.filter_by(id=review_id).first()
        
        if not review:
            response = make_response({"message": f"Review id {review_id} not found."}, 200)
            return response
        
        if review.user_id != session['user_id']:
            return {'error': 'Forbidden: You can only edit your own reviews'}, 403
        
        db.session.delete(review)
        db.session.commit()
        
        response = make_response({"message": f"Review id {review_id} deleted successfully."})
        
        return response


api.add_resource(ModifyItemReviewById, '/api/items/reviews/<int:review_id>', endpoint="modifyItemReviewsById")


@app.route('/api/item/item_id/<int:item_id>/average_rating', methods=['GET'])
def average_item_ratings(item_id):
    item_reviews = Review.query.filter_by(item_id=item_id).all()
    
    if not item_reviews:
        return jsonify({"average_rating": None, "message": "No reviews for this item"}), 404
    
    total_rating = 0
    
    for review in item_reviews:
        total_rating += review.rating
        
    average_rating = total_rating / len(item_reviews)
    average_rating = round(average_rating, 1)
    
    return jsonify({"average_rating": average_rating}), 200


@app.route("/api/items/daily_deals", methods=["GET"])
def daily_deals_items():
    items_list = [item.to_dict() for item in Item.query.join(Item.special_categories).filter(SpecialCategory.name == "daily_deals").all()]
        
    if items_list:  
        return make_response(jsonify(items_list), 200)
    
    return jsonify({"message": "No offer items in Daily Deals section."}, 404)


@app.route("/api/items/hot_&_new", methods=["GET"])
def hot_n_new_items():
    items_list = [item.to_dict() for item in Item.query.join(Item.special_categories).filter(SpecialCategory.name == "hot_&_new").all()]
        
    if items_list:  
        return make_response(jsonify(items_list), 200)
    
    return jsonify({"message": "No offer items in Hot & New section."}, 404)


@app.route("/api/items/season_offers", methods=["GET"])
def season_offers_items():
    items_list = [item.to_dict() for item in Item.query.join(Item.special_categories).filter(SpecialCategory.name == "season_offers").all()]
        
    if items_list:  
        return make_response(jsonify(items_list), 200)
    
    return jsonify({"message": "No offer items in Season Offers section."}, 404)


@app.route("/api/items/best_sellers", methods=["GET"])
def best_sellers_items():
    items_list = [item.to_dict() for item in Item.query.join(Item.special_categories).filter(SpecialCategory.name == "best_sellers").all()]
        
    if items_list:  
        return make_response(jsonify(items_list), 200)
    
    return jsonify({"message": "No offer items in Best Sellers section."}, 404)


if __name__== '__main__':
    port = int(os.environ.get("PORT", 5555)) 
    app.run(host="0.0.0.0", port=port, debug=True)
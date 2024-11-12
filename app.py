from flask import Flask, jsonify, request, render_template, make_response
from models import db, Item, SpecialCategory, User
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from flask_restful import Api, Resource
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://groupthree:phase5group3@localhost/electrohub_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
CORS(app, supports_credentials=True)

@app.route('/')
def index():
    return "<h1>Welcome to Electrohub</h1>"

class CrudItems(Resource):#Caleb
    def get(self):
        pass
    
    #Add 'Create Item button' in the frontend
    #Create, Update, Delete only for Admin
    def post(self):
        pass
    
    def patch(self):
        pass
    
    def delete(self):
        pass
    
api.add_resource(CrudItems, '/api/items', endpoint="crudItems")


@app.route('/api/item/item_details/<int:item_id>', methods=["GET"])
def get_item_details(item_id):#Caleb
    pass


@app.route("/api/item/<int:item_id>/add_special_category", methods=["POST"])
def add_special_category_to_item(item_id):#Shalyne
    data = request.json
    special_category_name = data["special_category_name"]
    
    item = Item.query.get(item_id)
    special_category = SpecialCategory.query.filter_by(name=special_category_name).first()

    if special_category and item:
        item.special_categories.append(special_category)
        db.session.commit()
        return jsonify({"message": f"Special Category {special_category_name} added to item"}), 200
    
    return jsonify({"message": "Error: Item or Special Category not found"}), 404


@app.route("/api/item/<int:item_id>/remove_special_category", methods=["POST"]) #Is the method POST or DELETE?
def remove_special_category_from_item(item_id):#Shalyne
    data = request.json
    special_category_name = data["special_category_name"]
    
    item = Item.query.get(item_id)
    special_category = SpecialCategory.query.filter_by(name=special_category_name).first()

    if special_category and item:
        item.special_categories.remove(special_category)
        db.session.commit()
        return jsonify({"message": f"Special Category {special_category_name} removed from item"}), 200
    
    return jsonify({"message": "Error: Item or Special Category not found"}), 404


class ItemReviews(Resource): #Caleb
    def get(self):
        pass
    
    # A user should be signed In to be able to POST, PATCH, DELETE a review
    def post(self):
        pass
    
    def patch(self):
        pass
    
    def delete(self):
        pass

api.add_resource(ItemReviews, '/api/items/<int:item_id>/reviews', endpoint="itemReviews")


@app.route('/api/item/<int:item_id>/average_rating', methods=['GET'])
def average_item_ratings(item_id):#Caleb
    pass
    

# Check items available for a specific item
@app.route("/api/item/<int:item_id/items_in_stock")
def items_in_stock_for_items(item_id): #Shalyne
    pass
    

if __name__ == '__main__':
    app.run(port=5555, debug=True)
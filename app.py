from flask import Flask, jsonify, request, render_template, make_response
from models import db, Item, SpecialCategory, User
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from flask_restful import Api, Resource
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://groupthree:group3@localhost/electrohub_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
CORS(app, supports_credentials=True)

@app.route('/')
def index():
    return "<h1>Welcome to Electrohub</h1>"


@app.route("/api/item/<int:item_id>/add_special_category", methods=["POST"])
def add_special_category_to_item(item_id):
    data = request.json
    special_category_name = data["special_category_name"]
    
    item = Item.query.get(item_id)
    special_category = SpecialCategory.query.filter_by(name=special_category_name).first()

    if special_category and item:
        item.special_categories.append(special_category)
        db.session.commit()
        return jsonify({"message": f"Item id {item.id} {item.item_name} added to special Category {special_category_name}"}), 200
    
    return jsonify({"message": "Error: Item or Special Category not found"}), 404


@app.route("/api/item/<int:item_id>/remove_special_category", methods=["DELETE"])
def remove_special_category_from_item(item_id):
    data = request.json
    special_category_name = data["special_category_name"]
    
    item = Item.query.get(item_id)
    special_category = SpecialCategory.query.filter_by(name=special_category_name).first()

    if special_category and item:
        item.special_categories.remove(special_category)
        db.session.commit()
        return jsonify({"message": f"Item id {item.id} {item.item_name} removed from special Category {special_category_name}"}), 200
    
    return jsonify({"message": "Error: Item or Special Category not found"}), 404



# Check items available for a specific item
@app.route("/api/item/<int:item_id>/items_in_stock", methods=["GET"])
def items_in_stock_for_items(item_id):

    item = Item.query.get(item_id)
    
    if item:
        return jsonify({"item_name": item.item_name, "items_in_stock": item.items_in_stock}), 200
    else:
        return jsonify({"message": "Item not found"}), 404

    

if __name__ == '__main__':
    app.run(port=5555, debug=True)
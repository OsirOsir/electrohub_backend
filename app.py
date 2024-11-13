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

class CrudItems(Resource):#Caleb
    def get(self):
        items_list = [item.to_dict() for item in Item.query.all()]
        
        if not items_list:
            response = make_response({"message": "No items available"}, 404,)
            return response
        
        response = make_response(items_list, 200,)
        return response
    
    #Add 'Create Item button' in the frontend
    #Create, Update, Delete only for Admin
    def post(self):
        try:
            item_name = request.json['item_name']
            item_features = request.json['item_features']
            item_price = request.json['item_price']
            item_image_url = request.json['item_image_url']
            item_category = request.json['item_category'] #Validate category to be among the provided categories
            items_in_stock = request.json['items_in_stock']
            
            new_item = Item(item_name= item_name, item_features=item_features, item_price= item_price, item_image_url= item_image_url, item_category=item_category, items_in_stock= items_in_stock)
            
            db.session.add(new_item)
            db.session.commit()
            
            response = make_response(new_item.to_dict(), 201,)
            return response
        
        except KeyError as e:
            return jsonify({"message": f"Missing required field: {str(e)}"}), 400
        
        except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    
    def patch(self):
        pass
    
    def delete(self):
        pass
    
api.add_resource(CrudItems, '/api/items', endpoint="crudItems")


@app.route('/api/item/item_details/item_id/<int:item_id>', methods=["GET"])
def get_item_details(item_id):#Caleb
    
    item = Item.query.filter_by(id=item_id).first()
    
    if not item:
        return jsonify({"message": f"Item id {item_id} not found"}), 404
    
    response = make_response(item.to_dict(), 200,)
    return response


@app.route('/api/items/reviews', methods=['GET'])
def get_all_reviews(self):
    pass


class ItemReviewsById(Resource): #Caleb
    def get(self):
        pass
    
    # A user should be signed In to be able to POST, PATCH, DELETE a review
    def post(self):
        pass
    
    def patch(self):
        pass
    
    def delete(self):
        pass

api.add_resource(ItemReviewsById, '/api/items/item_id/<int:item_id>/reviews', endpoint="itemReviewsById")


@app.route('/api/item/item_id/<int:item_id>/average_rating', methods=['GET'])
def average_item_ratings(item_id):#Caleb
    pass
    

if __name__ == '__main__':
    app.run(port=5555, debug=True)
    

    

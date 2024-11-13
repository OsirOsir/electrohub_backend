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

class CrudItems(Resource):
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

            # Create a dictionary for the response
            response_data = {
                'id': new_item.id,
                'item_name': new_item.item_name,
                'item_features': item_features,  # Ensure item_features is JSON-serializable
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


class CrudItemById(Resource):
    
    def patch(self, item_id):
        
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
        
        item = Item.query.filter(Item.id == item_id).first()
        
        if not item:
            response_dict = {"message": f"Item id {item_id} not found"}
            return make_response(response_dict, 404)
        
        #Ask if they are sure that they would like to delete the item
        db.session.delete(item)
        db.session.commit()
        
        response_dict = {"message": f"Item id {item.id} {item.item_name} has been deleted successfully"}
        
        return make_response(response_dict, 200)
    
api.add_resource(CrudItems, '/api/items/item_id/<int:item_id>', endpoint="crudItemsById")


@app.route('/api/item/item_details/item_id/<int:item_id>', methods=["GET"])
def get_item_details(item_id):
    
    item = Item.query.filter_by(id=item_id).first()
    
    if not item:
        return jsonify({"message": f"Item id {item_id} not found"}), 404
    
    response = make_response(item.to_dict(), 200,)
    return response


@app.route('/api/items/reviews', methods=['GET'])
def get_all_reviews(self):
    pass


class ItemReviewsById(Resource):
    def get(self, item_id):
        pass
    
    # A user should be signed In to be able to POST, PATCH, DELETE a review
    def post(self, item_id):
        pass
    
    def patch(self, item_id):
        pass
    
    def delete(self, item_id):
        pass

api.add_resource(ItemReviewsById, '/api/items/item_id/<int:item_id>/reviews', endpoint="itemReviewsById")


@app.route('/api/item/item_id/<int:item_id>/average_rating', methods=['GET'])
def average_item_ratings(item_id):
    pass
    

if __name__ == '__main__':
    app.run(port=5555, debug=True)
    


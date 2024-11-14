from flask import Flask, jsonify, request, render_template, make_response
from models import db, Item, SpecialCategory, User, Review
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
    #Create, Update, Delete only for Admin and when logged in
    def post(self):
        #Add constraints and validations to the fields when POSTing new review, all the required fields should be filled and descriptive messages in case of errors
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
    
api.add_resource(CrudItemsById, '/api/items/item_id/<int:item_id>', endpoint="crudItemsById")


@app.route('/api/item/item_details/item_id/<int:item_id>', methods=["GET"])
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
    
    # A user should be signed In to be able to POST, PATCH, DELETE a review
    def post(self, item_id):
        #Add constraints and validations to the fields when POSTing new review, all the required fields should be filled and descriptive messages in case of errors
        try:
            rating = request.json['rating']
            review_message = request.json['review_message']
            user_id = request.json['user_id']
            # item_id = item_id
            
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
            
api.add_resource(ItemReviewsById, '/api/items/item_id/<int:item_id>/reviews', endpoint="itemReviewsById")
    
class ModifyItemReviewById(Resource):
    #Add constraints and validations to the fields when PATCHing new review, all the required fields should be filled and descriptive messages in case of errors
    def patch(self, review_id):
        review = Review.query.filter(Review.id == review_id).first()
        
        if not review:
            return make_response({"message": f"Review id {review_id} not found"})
        
        for attr in request.json:
            if hasattr(review, attr):
                setattr(review, attr, request.json[attr])
                
        db.session.add(review)
        db.session.commit()
        
        return make_response(jsonify(review.to_dict()), 200)
    
    
    def delete(self, review_id):
        review = Review.query.filter_by(id=review_id).first()
        
        if not review:
            response = make_response({"message": f"Review id {review_id} not found."}, 200)
            return response
        
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
    

if __name__ == '__main__':
    app.run(port=5555, debug=True)
    


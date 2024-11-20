import pytest
from app import app, db
from models import Item, SpecialCategory, User, Review

@pytest.fixture(scope="module")
def test_client():
    # Set up the test database here (preferably using a separate test database)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://groupthree:group3@localhost/test_electrohub_db'
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Create the tables and initialize the app
    with app.app_context():
        db.create_all()

    # Create a test client for making requests
    client = app.test_client()
    yield client

    # Clean up the test database
    with app.app_context():
        db.drop_all()

@pytest.fixture(scope="module")
def init_db():
    # Create the test data here
    with app.app_context():
        # Add test data to your database
        special_category = SpecialCategory(name="hot_&_new")
        db.session.add(special_category)

        # Create test items and users
        item = Item(item_name="Test Item", item_price=100, items_in_stock=10, item_category="Smartphone")
        db.session.add(item)

        user = User(username="admin", password="password", role="Admin")
        db.session.add(user)

        db.session.commit()

    yield db  # This will make the database accessible in tests

    # Clean up test data after test execution
    with app.app_context():
        db.session.remove()
        db.drop_all()

def test_add_special_category(test_client, init_db):
    # Test that adding a special category to an item works

    item_id = 1  # Assuming we have item with ID 1
    special_category_name = "hot_&_new"

    # Simulate the POST request
    response = test_client.post(f"/api/item/{item_id}/add_special_category", json={"special_category_name": special_category_name})

    # Check the response
    assert response.status_code == 200
    assert b"added to special Category" in response.data


def test_remove_special_category(test_client, init_db):
    # Test that removing a special category from an item works

    item_id = 1  # Assuming we have item with ID 1
    special_category_name = "hot_&_new"

    # First, add the special category
    test_client.post(f"/api/item/{item_id}/add_special_category", json={"special_category_name": special_category_name})

    # Now, remove it
    response = test_client.delete(f"/api/item/{item_id}/remove_special_category", json={"special_category_name": special_category_name})

    # Check the response
    assert response.status_code == 200
    assert b"removed from special Category" in response.data


def test_get_item_details(test_client, init_db):
    item_id = 1  # Assuming we have item with ID 1

    # Test GET request to retrieve item details
    response = test_client.get(f"/api/item_details/item_id/{item_id}")

    assert response.status_code == 200
    assert b"item_name" in response.data
    assert b"items_in_stock" in response.data

def test_create_item(test_client, init_db):
    # Simulate admin login
    with test_client.session_transaction() as session:
        session['user_id'] = 1  # Assuming the user with ID 1 is an Admin

    # Create item
    response = test_client.post("/api/items", json={
        "item_name": "New Item",
        "item_features": "Feature 1",
        "item_price": 150,
        "item_image_url": "http://example.com/image.jpg",
        "item_category": "Smartphone",
        "items_in_stock": 20
    })

    assert response.status_code == 201
    assert b"New Item" in response.data

def test_unauthorized_create_item(test_client, init_db):
    # Simulate non-admin login
    with test_client.session_transaction() as session:
        session['user_id'] = 2  # Assuming the user with ID 2 is not an Admin

    # Attempt to create an item
    response = test_client.post("/api/items", json={
        "item_name": "New Item",
        "item_features": "Feature 1",
        "item_price": 150,
        "item_image_url": "http://example.com/image.jpg",
        "item_category": "Smartphone",
        "items_in_stock": 20
    })

    assert response.status_code == 403  # Forbidden
    assert b"Only admins can perform this action" in response.data


def test_average_item_rating(test_client, init_db):
    item_id = 1  # Assuming we have item with ID 1

    # Add reviews for the item
    test_client.post(f"/api/item_id/{item_id}/reviews", json={"rating": 5, "review_message": "Great item!"})
    test_client.post(f"/api/item_id/{item_id}/reviews", json={"rating": 4, "review_message": "Good item."})

    # Test average rating
    response = test_client.get(f"/api/item/item_id/{item_id}/average_rating")

    assert response.status_code == 200
    assert b"average_rating" in response.data
    assert b"4.5" in response.data  # Based on the added reviews


def login(client, user_id):
    """Helper function to log in a user"""
    with client.session_transaction() as sess:
        sess['user_id'] = user_id


def test_get_all_reviews(client):
    """Test retrieving all reviews"""
    response = client.get('/api/items/reviews')
    assert response.status_code == 200
    assert 'No reviews available' in response.json['message']
    
def test_get_reviews_for_item(client):
    """Test retrieving reviews for a specific item"""
    login(client, 1)  # Log in as admin
    
    # Add a review for item with ID 1
    client.post('/api/item_id/1/reviews', json={
        "rating": 4,
        "review_message": "Good item, but a bit overpriced"
    })
    
    response = client.get('/api/item_id/1/reviews')
    assert response.status_code == 200
    assert len(response.json) == 1  # One review added
    assert response.json[0]['review_message'] == "Good item, but a bit overpriced"


def test_patch_review(client):
    """Test updating a review by review ID"""
    login(client, 1)  # Log in as admin

    # Add a review for item with ID 1
    response = client.post('/api/item_id/1/reviews', json={
        "rating": 3,
        "review_message": "Average product"
    })
    review_id = response.json['id']

    # Patch the review
    patch_response = client.patch(f'/api/items/reviews/{review_id}', json={
        "rating": 4,
        "review_message": "Better than expected!"
    })

    assert patch_response.status_code == 200
    assert patch_response.json['rating'] == 4
    assert patch_response.json['review_message'] == "Better than expected!"
    
def test_average_item_ratings(client):
    """Test getting the average rating for an item"""
    # Add reviews for item with ID 1
    login(client, 1)  # Log in as admin
    client.post('/api/item_id/1/reviews', json={"rating": 4, "review_message": "Good product"})
    client.post('/api/item_id/1/reviews', json={"rating": 5, "review_message": "Excellent!"})
    
    response = client.get('/api/item/item_id/1/average_rating')
    
    assert response.status_code == 200
    assert response.json['average_rating'] == 4.5  # Average of 4 and 5


def test_average_item_ratings_no_reviews(client):
    """Test getting the average rating for an item that has no reviews"""
    response = client.get('/api/item/item_id/1/average_rating')
    assert response.status_code == 404
    assert response.json['message'] == 'No reviews for this item'
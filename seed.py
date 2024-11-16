from models import db, User, Product, Cart  # Ensure Cart is imported
from app import app
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

def create_users():
    """Create and return admin and regular users."""
    admin_user = User(
        name="AdminUser", 
        email="admin@example.com", 
        role="admin"
    )
    admin_user.password = "adminpassword"  

    regular_user = User(
        name="RegularUser", 
        email="user@example.com", 
        role="user"
    )
    regular_user.password = "userpassword"  

    regular_user1 = User(
        name="RegularUser1", 
        email="user1@example.com", 
        role="user"
    )
    regular_user1.password = "userpassword1"  

    return admin_user, regular_user, regular_user1

def create_products(admin_user):
    """Create electronics products associated with the admin user."""
    products = [
        Product(
            name="Laptop", 
            description="A powerful laptop for professionals.", 
            price=1099, 
            item_availability=50, 
            user_id=admin_user.id  
        ),
        Product(
            name="Smartphone", 
            description="A high-end smartphone with all the latest features.", 
            price=899, 
            item_availability=100, 
            user_id=admin_user.id
        ),
        Product(
            name="Headphones", 
            description="Noise-canceling headphones for an immersive experience.", 
            price=199, 
            item_availability=75, 
            user_id=admin_user.id
        )
    ]
    return products


def seed_data():
    """Seed the database with sample data."""
    try:
        
        admin_user, regular_user, regular_user1 = create_users()
        db.session.add(admin_user)
        db.session.add_all([regular_user, regular_user1])

        
        db.session.commit()

        
        products = create_products(admin_user)
        db.session.add_all(products)
        db.session.commit()

        
        add_cart_items_for_user(regular_user, products)  
        add_cart_items_for_user(regular_user1, products)  

        
        db.session.commit()

        print("Database seeded successfully with Admin, Users, Products, and Cart Items!")

    except IntegrityError as ie:
        print(f"Integrity error occurred: {ie}")
        db.session.rollback()  

    except Exception as e:
        print(f"An error occurred while seeding the database: {e}")
        db.session.rollback()


def add_cart_items_for_user(user, products):
    """Add sample cart items for a user."""
    cart_items = [
        Cart(user_id=user.id, product_id=products[0].id, quantity=2),  
        Cart(user_id=user.id, product_id=products[1].id, quantity=1)   
    ]
    db.session.add_all(cart_items)

# Set up and seed the database
with app.app_context():
    try:
        
        db.drop_all()  
        db.create_all()  
        seed_data() 

    except Exception as e:
        print(f"An error occurred while setting up the database: {e}")
        db.session.rollback()

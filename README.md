# electrohub_backend


def add_cart_items_for_user(user, item):
        """Add sample cart items for a user."""
        cart_items = [
            Cart(user_id=user.id, item_id=1, quantity=2),  
            Cart(user_id=user.id, item_id=2, quantity=1)   
        ]
        db.session.add_all(cart_items)
        db.session.commit()
        return cart_items
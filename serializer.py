def user_serializer(user):
    """Serialize a user and include their cart items."""
    return {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'is_admin': user.is_admin(), 
        'role': user.role,
        'cart_items': [cart_item_serializer(cart_item) for cart_item in user.cart_items]  
    }

def product_serializer(product):
    """Serialize a product and include cart items that reference it."""
    return {
        'id': product.id,
        'name': product.name,
        'price': str(product.price),  
        'description': product.description,
        'item_availability': product.item_availability,
        'user_id': product.user_id,
        'cart_items': [cart_item_serializer(cart_item) for cart_item in product.cart_items]  
    }

def cart_item_serializer(cart_item):
    """Serialize a cart item."""
    return {
        'user_id': cart_item.user_id,
        'product_id': cart_item.product_id,
        'quantity': cart_item.quantity
    }

def user_serializer(user):
    """Serialize a user and include their cart items."""
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin(), 
        'role': user.role,
        'cart_items': [cart_item_serializer(cart_item) for cart_item in user.cart_items]  
    }

def item_serializer(items):
    """Serialize a item and include cart items that reference it."""
    return {
        'id': items.id,
        'item_name': items.item_name,
        'item_price': str(items.item_price),  
        'item_features': items.item_features,
        'items_in_stock': items.items_in_stock,
        'item_prev_price' :items.item_prev_price,
        'item_image_url':items.item_image_url,
        'item_category' :items.item_category,
        'user_id': items.user_id,
        'cart_items': [cart_item_serializer(cart_item) for cart_item in items.cart_items]  
    }

def cart_item_serializer(cart_item):
    """Serialize a cart item."""
    return {
        'user_id': cart_item.user_id,
        'item_id': cart_item.item_id,
        'quantity': cart_item.quantity
    }

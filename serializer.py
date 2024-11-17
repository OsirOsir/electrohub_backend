def user_serializer(user):
    """Serialize a user and include their cart items."""
    return {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role,
        'is_admin': user.is_admin(),
        'is_active': user.is_active,
        'cart_items': [cart_item_serializer(cart_item) for cart_item in user.cart_items],
        'items': [item_serializer(item) for item in user.items]  # Include user's items as well
    }

def item_serializer(item):
    """Serialize an item and include cart items that reference it."""
    return {
        'id': item.id,
        'item_name': item.item_name,
        'item_price': str(item.item_price),  # Price as string to handle currency formatting
        'item_description': item.item_features.get('description', ''),  # Assume item_features contains description
        'item_availability': item.is_in_stock(),
        'owner_id': item.owner.id if item.owner else None,  # Reference to owner ID if exists
        'special_categories': [category.name for category in item.special_categories],
        'cart_items': [cart_item_serializer(cart_item) for cart_item in item.cart_items]
    }

def cart_item_serializer(cart_item):
    """Serialize a cart item."""
    return {
        'id': cart_item.id,  # Include cart item ID
        'user_id': cart_item.user_id,
        'item_id': cart_item.item_id,  # Correct field names
        'quantity': cart_item.quantity,
        'item': item_serializer(cart_item.item)  # Include item details for better context
    }

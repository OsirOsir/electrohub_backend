def user_serializer(user):
    return {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'is_admin': user.is_admin(),
        'role': user.role,
    }

def product_serializer(product):
    return {
        'id': product.id,
        'name': product.name,
        'price': str(product.price),  
        'description': product.description,
        'item_availability': product.item_availability,
        'user_id': product.user_id,
    }
from item.models import FavoriteItem  

def cart_and_follow_counts(request):
    cart_count = len(request.session.get('cart', []))
    follow_count = FavoriteItem.objects.count()

    return {
        'cart_count': cart_count,
        'follow_count': follow_count,
    }

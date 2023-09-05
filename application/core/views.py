import json
from django.shortcuts import render, redirect, get_object_or_404
from item.models import Format, Item, Image, FavoriteItem
from .forms import SingupFrom

def home(request):
    items = Item.objects.filter(is_sold=False)[::-1][:6]
    images = [Image.objects.filter(item_id=item.pk).first() for item in items]
    newest_items = zip(items, images)
    formats = Format.objects.all()
    count = len(request.session['cart']) if 'cart' in request.session else 0

    return render(request, 'core/home.html', {
        'formats': formats,
        'newest_items': newest_items,
        'count': count
    })

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == "POST":
        form = SingupFrom(request.POST)
        
        if form.is_valid():
            form.save()

            return redirect("/login/")
    else:
        form = SingupFrom()
    
    return render(request, 'core/signup.html', {
        "form": form
    })

def cart(request):
    if 'cart' not in request.session:
        request.session['cart'] = []  

    if request.method == 'POST' and 'item_id' in request.POST:
        add_to_cart(request)
        
    return render(request, 'core/cart.html', {
        'cart': request.session['cart'],
        'count': len(request.session['cart'])
    })


def add_to_cart(request):
    item_id = request.POST['item_id']
    item = get_object_or_404(Item, id=item_id)
    image = Image.objects.filter(item_id=item.pk).first()

    item_data = {
        'id': item.id,
        "image": str(image.url),
        'name': item.name,
        'price': item.price,
    }

    cart = request.session['cart']
    if item_data not in cart:
        cart.append(item_data)
        request.session.modified = True

def remove_from_cart(request, item_id):
    if 'cart' in request.session:
        cart = request.session['cart']
        cart = [item for item in cart if item['id'] != item_id]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('core:user-cart')

def favorite(request):
    favorite_items = FavoriteItem.objects.all()
    
    return render(request, 'core/favorite.html', {
        'favorite_items': favorite_items,
    })
import json
from django.shortcuts import render, redirect, get_object_or_404
from item.models import Category, Item, Image
from .forms import SingupFrom

def home(request):
    items = Item.objects.filter(is_sold=False)[::-1][:6]
    images = [Image.objects.filter(item_id=item.pk).first() for item in items]
    
    newest_items = zip(items, images)
        
    categories = Category.objects.all()
    return render(request, 'core/home.html', {
        'categories': categories,
        'newest_items': newest_items,
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
        cart.append(item_data)
        request.session.modified = True

    return render(request, 'core/cart.html', {
        'cart': request.session['cart'],
    })

def remove_from_cart(request, item_id):
    if 'cart' in request.session:
        cart = request.session['cart']
        for item in cart:
            if item['id'] == item_id:
                cart.remove(item)
                request.session.modified = True
                break
    return redirect('core:user-cart')

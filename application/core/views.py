from django.shortcuts import render, redirect
from item.models import Category, Item, Image
from .forms import SingupFrom

def home(request):
    items = Item.objects.filter(is_sold=False)[:6]
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
    

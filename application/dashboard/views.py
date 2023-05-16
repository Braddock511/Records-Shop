from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from item.models import Item, Image

@login_required
def index(request):
    filter_items = Item.objects.filter(created_by=request.user)
    images = [Image.objects.filter(item_id=item.pk).first() for item in filter_items]
    
    items = zip(filter_items, images)
    
    
    return render(request, "dashboard/index.html", {
        "items": items
    })
    
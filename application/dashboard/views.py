from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from item.models import Item, Image, GENRES


@login_required
def user_items(request):
    filter_items = Item.objects.filter(created_by=request.user)

    # Name filter
    if name := request.GET.get('offername', ''):
        filter_items = filter_items.filter(Q(name__icontains=name))

    # Format filter
    if format_filter := request.GET.get('format', ''):
        filter_items = filter_items.filter(format=format_filter)
        
    # Price filter
    if min_price := request.GET.get('min_price', ''):
        filter_items = filter_items.filter(price__gte=min_price)

    if max_price := request.GET.get('max_price', ''):
        filter_items = filter_items.filter(price__lte=max_price)

    # Genre filter
    if genre_filter := request.GET.get('genre', '').lower():
        filter_items = filter_items.filter(genre=genre_filter)

    # Carton filter
    if carton_filter := request.GET.get('carton', '').upper():
        filter_items = filter_items.filter(carton=carton_filter)

    filter_items = filter_items[::-1] # Reverse to the latest offer  
    images = [Image.objects.filter(item_id=item.pk).first() for item in filter_items]

    items = list(zip(filter_items, images))

    paginator = Paginator(items, 20)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "dashboard/user-items.html", {
        "page_obj": page_obj,
        "format_filter": format_filter,
        "min_price": min_price,  
        "max_price": max_price,
        "genres": GENRES,
        "genre_filter": genre_filter,
        "carton_filter": carton_filter
    })
    
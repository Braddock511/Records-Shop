from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from item.models import Item, Image, GENRES


@login_required
def user_items(request):
    filter_items = Item.objects.filter(created_by=request.user)[::-1]

    # Name filter
    name = request.GET.get('offername', '')

    if name:
        filter_items = filter_items.filter(Q(name__icontains=name))

    # Format filter
    format_filter = request.GET.get('format', '')

    if format_filter:
        filter_items = filter_items.filter(category=format_filter)
        
    # Price filter
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    if min_price:
        filter_items = filter_items.filter(price__gte=min_price)

    if max_price:
        filter_items = filter_items.filter(price__lte=max_price)

    # Genre filter
    genre_filter = request.GET.get('genre', '')

    if genre_filter:
        filter_items = filter_items.filter(genre=genre_filter.lower())

    # Carton filter
    carton_filter = request.GET.get('carton', '').upper()
    if carton_filter:
        filter_items = filter_items.filter(carton=carton_filter)

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
    
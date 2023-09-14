from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from random import randint
from .forms import NewItemForm, EditItemForm, FileFieldForm
from django.views.generic.edit import FormView
from .models import Item, Image, FavoriteItem, GENRES

MAX_IMAGES = 6

def sort_items(items, sort_by):
    if sort_by == 'latest_offer':
        return sorted(items, key=lambda x: x.created_at, reverse=True)
    elif sort_by == 'lowest_price':
        return sorted(items, key=lambda x: x.price)
    elif sort_by == 'highest_price':
        return sorted(items, key=lambda x: x.price, reverse=True)
    
    return items

def items(request):
    filter_items = Item.objects.all()

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
    if genre_filter := request.GET.get('genre', ''):
        filter_items = filter_items.filter(genre=genre_filter)

    # Carton filter
    if carton_filter := request.GET.get('carton', '').upper():
        filter_items = filter_items.filter(carton=carton_filter)

    if sort_by := request.GET.get('sort-by', ''):
        filter_items = sort_items(filter_items, sort_by)
    
    images = [Image.objects.filter(item_id=item.pk).first() for item in filter_items]

    items = list(zip(filter_items, images))

    paginator = Paginator(items, 20)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "item/items.html", {
        "page_obj": page_obj,
        "query": name,
        "format_filter": format_filter,
        "min_price": min_price,  
        "max_price": max_price,
        "genres": GENRES,
        "genre_filter": genre_filter,
        "sort_by": sort_by,
    })    

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    images = Image.objects.filter(item_id=pk)
    
    random_offers = randint(0, len(Item.objects.filter(is_sold=False))-6) if len(Item.objects.filter(is_sold=False)) > 6 else 0
    filter_related_items = Item.objects.filter(format=item.format, is_sold=False).exclude(pk=pk)[random_offers:random_offers+6]
    related_images = [Image.objects.filter(item_id=item.pk).first() for item in filter_related_items]
    related_items = zip(filter_related_items, related_images)
    is_followed = FavoriteItem.objects.filter(item_id=item).exists()
    
    return render(request, "item/detail.html", {
        "item": item,
        "images": images,
        'related_items': related_items,
        "is_followed": is_followed
    })

class NewItemFormView(FormView):
    form_class = NewItemForm
    success_url = "/"

    def form_valid(self, form):
        item = form.save(commit=False)
        item.created_by = self.request.user
        item.save()

        images = self.request.FILES.getlist("images")
        for image in images:
            Image.objects.create(item=item, url=image)

        return super().form_valid(form)

@login_required
def new_item(request):
    if request.method == "POST":
        form = NewItemForm(request.POST, request.FILES)
        if len(request.FILES.getlist("images")) <= MAX_IMAGES and form.is_valid():
            return NewItemFormView.as_view()(request)
        
        image_form = FileFieldForm()
        
        if len(request.FILES.getlist("images")) > MAX_IMAGES:
            messages.warning(request, "Maksymalnie 6 zdjęć na ofertę")
    else:
        form = NewItemForm()
        image_form = FileFieldForm()

    return render(request, 'item/form.html', {
        "form": form,
        "imageForm": image_form,
        "max_images": MAX_IMAGES,
        "title": "Nowa oferta"
    })
    
@login_required
def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    old_images = Image.objects.filter(item_id=item.pk).all()

    if request.method == "POST":
        form = EditItemForm(request.POST, request.FILES, instance=item)
        new_images = request.FILES.getlist("images")
        
        if form.is_valid() and len(request.FILES.getlist("images")) <= MAX_IMAGES:
            form.save()
            
            if new_images:
                for image in old_images:
                    image.delete()
                
                for image in new_images:
                    Image.objects.create(item=item, url=image)
            
            return redirect("item:detail", pk=item.id)
        else:
            image_form = FileFieldForm()
            messages.warning(request, "Maksymalnie 6 zdjęć na ofertę")
        
    else:
        form = EditItemForm(instance=item)
        image_form = FileFieldForm(initial={"images": old_images})
    
    return render(request, 'item/form.html', {
        "form": form,
        "imageForm": image_form,
        "max_images": MAX_IMAGES,
        "title": "Edytuj ofertę"
    })

@login_required
def edit_items(request):
    if request.method != 'POST':
        return
    
    selected_items = request.POST.getlist('selected-id-items')
    new_price = request.POST.get('new-price', '')
    new_carton = request.POST.get('new-carton', '')
    items = Item.objects.filter(id__in=selected_items)

    for item in items:
        if new_price:
            item.price = new_price
        if new_carton:
            item.carton =  new_carton
        item.save()

    return redirect('dashboard:user-items')  
  
@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()
    
    return redirect("dashboard:user-items")

@login_required
def toggle_favorite(request, pk):
    item = Item.objects.get(pk=pk)  

    try:
        favorite_item = FavoriteItem.objects.get(item_id=item)
        # If it exists, delete it
        favorite_item.delete()
    except FavoriteItem.DoesNotExist:
        # If it doesn't exist, create a new instance
        new_instance = FavoriteItem(item_id=item)
        new_instance.save()

    return redirect('item:detail', pk=pk)

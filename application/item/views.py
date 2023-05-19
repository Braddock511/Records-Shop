from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from random import randint
from .forms import NewItemForm, EditItemForm, FileFieldForm
from django.views.generic.edit import FormView
from .models import Item, Image, GENRES

MAX_IMAGES = 6

def items(request):
    filter_items = Item.objects.filter(is_sold=False)
    
    # Name filter
    query = request.GET.get('query', '')
    if query:
        filter_items = filter_items.filter(Q(name__icontains=query))
    
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
        
    images = [Image.objects.filter(item_id=item.pk).first() for item in filter_items]
    items = list(zip(filter_items, images))

    paginator = Paginator(items, 20)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "item/items.html", {
        "page_obj": page_obj,
        "query": query,
        "format_filter": format_filter,
        "min_price": min_price,  
        "max_price": max_price,
        "genres": GENRES,
        "genre_filter": genre_filter,
    })    

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    images = Image.objects.filter(item_id=pk)
    
    random_offers = randint(0, len(Item.objects.filter(is_sold=False))-6)
    filter_related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[random_offers:random_offers+6]
    related_images = [Image.objects.filter(item_id=item.pk).first() for item in filter_related_items]
    related_items = zip(filter_related_items, related_images)
    
    return render(request, "item/detail.html", {
        "item": item,
        "images": images,
        'related_items': related_items
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
        if form.is_valid() and len(request.FILES.getlist("images")) <= MAX_IMAGES:
            return NewItemFormView.as_view()(request)
        else:
            image_form = FileFieldForm()
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
        image_form = FileFieldForm()
    
    return render(request, 'item/form.html', {
        "form": form,
        "imageForm": image_form,
        "max_images": MAX_IMAGES,
        "title": "Edytuj ofertę"
    })
    
@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()
    
    return redirect("dashboard:user-items")
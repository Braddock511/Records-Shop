from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import NewItemForm, EditItemForm, ImageForm
from .models import Item, Category, Image

def items(request):
    filter_items = Item.objects.filter(is_sold=False)
    
    categories = Category.objects.all()
    
    query = request.GET.get('query', '')
    category_id = request.GET.get("category", 0)
    
    if category_id:
        filter_items = filter_items.filter(category_id=category_id)
    
    if query:
        filter_items = filter_items.filter(Q(name__icontains=query))
        
    images = [Image.objects.filter(item_id=item.pk).first() for item in filter_items]
    items = zip(filter_items, images)
    
    return render(request, "item/items.html", {
        "items": items,
        "query": query,
        "categories": categories,
        "category_id": int(category_id)
    })    

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    images = Image.objects.filter(item_id=pk)
    filter_related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[:6]
    related_images = [Image.objects.filter(item_id=item.pk).first() for item in filter_related_items]
    related_items = zip(filter_related_items, related_images)
    
    return render(request, "item/detail.html", {
        "item": item,
        "images": images,
        'related_items': related_items
    })
    
@login_required
def new_item(request):
    if request.method == "POST":
        form = NewItemForm(request.POST, request.FILES)
        images = request.FILES.getlist("image")
        
        if form.is_valid() and len(images) <= ImageForm.MAX_IMAGES:
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            
            for image in images:
                Image.objects.create(item=item, url=image)
            
            return redirect("item:detail", pk=item.id)
        else:
            image_form = ImageForm()
            messages.warning(request, "Max 6 images")
    else:
        form = NewItemForm()
        image_form = ImageForm()
    
    return render(request, 'item/form.html', {
        "form": form,
        "imageForm": image_form,
        "title": "Nowa oferta"
    })
    
@login_required
def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    old_images = Image.objects.filter(item_id=item.pk).all()

    if request.method == "POST":
        form = EditItemForm(request.POST, request.FILES, instance=item)
        new_images = request.FILES.getlist("image")
        
        if form.is_valid():
            form.save()
            
            for image in old_images:
                image.delete()
            
            for image in new_images:
                Image.objects.create(item=item, url=image)
            
            return redirect("item:detail", pk=item.id)
    else:
        form = EditItemForm(instance=item)
        image_form = ImageForm()
    
    return render(request, 'item/form.html', {
        "form": form,
        "imageForm": image_form,
        "title": "Edytuj ofertę"
    })
    
@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()
    
    return redirect("dashboard:index")
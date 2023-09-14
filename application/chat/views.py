import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render
from .models import Room, User

def index(request):
    return render(request, "chat.html")

@require_POST
def create_room(request, uuid):
    name = request.POST.get("name", "")
    url = request.POST.get("url", "")
    
    Room.objects.create(uuid=uuid, client=name, url=url)
    
    return JsonResponse({"message": "room created"})

@login_required
def chat_admin(request):
    rooms = Room.objects.all()
    users = User.objects.filter(is_staff=False)
    
    return render(request, 'chat-admin.html', {
        "rooms": rooms,
        "users": users,
    })
from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path("", views.index, name='chat'),
    path("create-room/<str:uuid>", views.create_room, name='create-room'),
    path("chat-admin/", views.chat_admin, name="chat-admin")
]
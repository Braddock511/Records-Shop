from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from item import views as item_views

app_name = 'dashboard'

urlpatterns = [
    path("", views.user_items, name='user-items'),
    path("<int:pk>/delete/", item_views.delete, name="delete"),
    path("<int:pk>/edit/", item_views.edit_item, name="edit"),
]

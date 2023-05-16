from django.urls import path
from . import views

app_name = "item"

urlpatterns = [
    path("", views.items, name="items"),
    path("new-item/", views.new_item, name="new-item"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/edit/", views.edit_item, name="edit"),
]
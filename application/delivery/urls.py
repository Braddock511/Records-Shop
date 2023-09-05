from django.urls import path
from . import views

app_name = "dostawa"

urlpatterns = [
    path('zamówienia/', views.parcels, name='parcels'),
    path('utworz-zamowienie/', views.create_parcel, name='create_parcel'),
    path('status-zamowienia/<str:parcel_number>/', views.parcel_status, name='parcel_status'),
]

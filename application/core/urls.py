from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

app_name = 'core'

urlpatterns = [
    path("", views.home, name='home'),
    path("cart/", views.cart, name='user-cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path("contact/", views.contact, name='contact'),
    path("signup/", views.signup, name='signup'),
    path("login/", auth_views.LoginView.as_view(template_name="core/login.html",authentication_form=LoginForm), name='login'),
]

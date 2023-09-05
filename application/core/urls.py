from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

app_name = 'core'

urlpatterns = [
    path("", views.home, name='home'),
    path("koszyk/", views.cart, name='user-cart'),
    path('koszyk/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path("ulubiony/", views.favorite, name='favorite'),
    path("kontakt/", views.contact, name='contact'),
    path("rejestracja/", views.signup, name='signup'),
    path("logowanie/", auth_views.LoginView.as_view(template_name="core/login.html",authentication_form=LoginForm), name='login'),
    path("wyloguj/", auth_views.LogoutView.as_view(next_page='core:login'), name='logout'),
]

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user_payment.views import stripe_webhook

urlpatterns = [
    path("", include('core.urls')),
    path("oferty/", include('item.urls')),
    path("dashboard/", include('dashboard.urls')),
    path("payment/", include('user_payment.urls')),
    path("chat/", include('chat.urls')),
	path('stripe_webhook', stripe_webhook, name='stripe_webhook'),
    path("dostawa/", include('delivery.urls')),
    path("admin/", admin.site.urls),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

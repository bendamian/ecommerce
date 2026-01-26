
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    #store app urls
    path('', include('store.urls', namespace='store_app')),
    #cart app urls
    path('cart/', include('cart.urls', namespace='cart_app')),
    #account app urls
    path('account/', include('account.urls', namespace='account_app')),
    #payment app urls
    path('payment/', include('payment.urls', namespace='payment_app')),
]


# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

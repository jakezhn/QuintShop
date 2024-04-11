from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include the 'shop' app URLs
    path('api/shop/', include('shop.urls')),  
]

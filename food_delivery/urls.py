from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('restaurant/', include('restaurant.urls')),
    path('user/', include('user.urls')),
    path('api/customer/', include('restaurant.api.customer_urls')),
    path('api/driver/', include('restaurant.api.driver_urls')),
    path('api/restaurant/', include('restaurant.api.restaurant_urls')),
    path('api/social/', include('rest_framework_social_oauth2.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

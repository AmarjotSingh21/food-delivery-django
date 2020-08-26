from django.urls import path
from .views import restaurant_home


urlpatterns = [
    path('', restaurant_home, name='restaurant-home'),
]
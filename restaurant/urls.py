from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import restaurant_home, restaurant_sign_up

app_name = 'restaurant'
urlpatterns = [
    path('', restaurant_home, name='home'),
]

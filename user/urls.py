from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import restaurant_home, restaurant_sign_up

app_name = 'user'
urlpatterns = [
    path('sign-up/', restaurant_sign_up, name='sign-up'),
    path('sign-in/', LoginView.as_view(template_name='restaurant/sign_in.html'),
         name='sign-in'),
    path('sign-out/', LogoutView.as_view(template_name='restaurant/sign_out.html'),
         name='sign-out'),
]

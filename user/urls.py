from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import sign_up_view

app_name = 'user'
urlpatterns = [
    path('sign-up/', sign_up_view, name='sign-up'),
    path('sign-in/', LoginView.as_view(template_name='user/sign_in.html'),
         name='sign-in'),
    path('sign-out/', LogoutView.as_view(template_name='user/sign_out.html'),
         name='sign-out'),
]

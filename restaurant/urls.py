from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import home_view, account_view, meal_view, order_view, report_view, sign_up_view, add_meal_view, edit_meal_view

app_name = 'restaurant'
urlpatterns = [
    path('', home_view, name='home'),
    path('sign-up/', sign_up_view, name='sign-up'),
    path('sign-in/', LoginView.as_view(template_name='restaurant/sign_in.html'),
         name='sign-in'),
    path('sign-out/', LogoutView.as_view(template_name='restaurant/sign_out.html'),
         name='sign-out'),
    path('account/', account_view, name='account'),
    path('meal/', meal_view, name='meal'),
    path('meal/add/', add_meal_view, name='add-meal'),
    path('meal/<int:meal_id>/edit/', edit_meal_view, name='edit-meal'),
    path('order/', order_view, name='order'),
    path('report/', report_view, name='report'),
]

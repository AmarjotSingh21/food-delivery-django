from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import home_view, account_view, meal_view, order_view, report_view

app_name = 'restaurant'
urlpatterns = [
    path('', home_view, name='home'),
    path('account/', account_view, name='account'),
    path('meal/', meal_view, name='meal'),
    path('order/', order_view, name='order'),
    path('report/', report_view, name='report'),
]

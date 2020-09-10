from django.urls import path

from .views import get_restaurants, get_meals, add_order, customer_get_latest_order


urlpatterns = [
    path('restaurants/', get_restaurants),
    path('meals/<int:restaurant_id>/', get_meals),
    path('order/add/', add_order),
    path('order/latest/', customer_get_latest_order),
]

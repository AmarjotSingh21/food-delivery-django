from django.urls import path

from .views import (customer_get_restaurants, customer_get_meals,
                    customer_add_order, customer_get_latest_order)


urlpatterns = [
    path('restaurants/', customer_get_restaurants),
    path('meals/<int:restaurant_id>/', customer_get_meals),
    path('order/add/', customer_add_order),
    path('order/latest/', customer_get_latest_order),
]

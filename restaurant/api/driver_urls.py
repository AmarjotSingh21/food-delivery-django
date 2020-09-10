from django.urls import path

from .views import (driver_get_ready_orders,
                    driver_pick_order, driver_get_latest_order,
                    driver_complete_order, driver_get_revenue)

urlpatterns = [
    path('orders/ready/', driver_get_ready_orders),
    path('order/pick/', driver_pick_order),
    path('order/latest/', driver_get_latest_order),
    path('order/complete/', driver_complete_order),
    path('order/latest/', driver_get_revenue),
]

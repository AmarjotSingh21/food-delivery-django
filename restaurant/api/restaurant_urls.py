from django.urls import path
from .views import restaurant_order_notification

urlpatterns = [
    path('order/notification/<str:last_request_time>/', restaurant_order_notification)
]

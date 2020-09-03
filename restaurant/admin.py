from django.contrib import admin
from .models import Restaurant, Meal, Order, OrderDetail

admin.site.register(Restaurant)
admin.site.register(Meal)
admin.site.register(Order)
admin.site.register(OrderDetail)
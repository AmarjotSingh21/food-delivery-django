from django.http import JsonResponse

from restaurant.models import Restaurant, Meal, Order, OrderDetail
from .serializers import RestaurantSerializer, MealSerializer


def get_restaurants(request):
    restaurants = Restaurant.objects.all().order_by('-id')
    json_data = RestaurantSerializer(restaurants, many=True, context={
                                     'request': request}).data
    return JsonResponse({'restaurants': json_data})


def get_meals(request, restaurant_id):
    meals = Meal.objects.filter(restaurant__id=restaurant_id).order_by('-id')
    json_data = MealSerializer(meals, many=True, context={
                               'request': request}).data
    return JsonResponse({'meals': json_data})


def add_order(request):
    return JsonResponse({})


def get_latest_order(request):
    return JsonResponse({})

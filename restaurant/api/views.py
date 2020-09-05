import json

from django.http import JsonResponse
from django.utils import timezone
from oauth2_provider.models import AccessToken
from django.views.decorators.csrf import csrf_exempt

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


@csrf_exempt
def add_order(request):
    """
        params:
            access_token
            restaurant_id
            address
            order_details ( json ), example:
                [{"meal_id":1, "quantity":2},
                {"meal_id":2, "quantity":1}]
            stripe_token
        return:
            {"status":"success"}
    """
    if request.method == "POST":
        # Get Token
        access_token = AccessToken.objects.get(
            token=request.POST.get("access_token"), expires__gt=timezone.now())

        # Get Profile
        customer = access_token.user.customer

        # Check whether customer has any order that is not delivered
        if Order.objects.filter(customer=customer).exclude(status=Order.DELIVERED):
            return JsonResponse({"status": "fail", "error": "Your last order must be completed"})

        # Check address
        if not request.POST['address']:
            return JsonResponse({"status": "failed", "error": "Address is required"})

        # Get order details
        order_details = json.loads(request.POST['order_details'])

        order_total = 0
        print(order_details)
        for meal in order_details:
            order_total += Meal.objects.get(
                id=meal['meal_id']).price * meal['quantity']
        if len(order_details) > 0:
            # Create order
            order = Order.objects.create(
                customer=customer, restaurant_id=request.POST['restaurant_id'],
                total=order_total, status=Order.COOKING,
                address=request.POST['address']
            )

            # Create order details
            for meal_data in order_details:
                print(meal_data)
                meal = Meal.objects.get(id=meal_data['meal_id'])
                quantity = meal_data['quantity']
                OrderDetail.objects.create(
                    order=order, meal=meal,
                    quantity=quantity, sub_total=meal.price * quantity
                )
            return JsonResponse({"status": "success"})


def get_latest_order(request):
    return JsonResponse({})

import json

from django.http import JsonResponse
from django.utils import timezone
from oauth2_provider.models import AccessToken
from django.views.decorators.csrf import csrf_exempt

from restaurant.models import Restaurant, Meal, Order, OrderDetail
from .serializers import RestaurantSerializer, MealSerializer, OrderSerializer

# * ##########
# * CUSTOMER
# * ##########


def customer_get_restaurants(request):
    restaurants = Restaurant.objects.all().order_by('-id')
    json_data = RestaurantSerializer(restaurants, many=True, context={
                                     'request': request}).data
    return JsonResponse({'restaurants': json_data})


def customer_get_meals(request, restaurant_id):
    meals = Meal.objects.filter(restaurant__id=restaurant_id).order_by('-id')
    json_data = MealSerializer(meals, many=True, context={
                               'request': request}).data
    return JsonResponse({'meals': json_data})


@csrf_exempt
def customer_add_order(request):
    """
        params: access_token, restaurant_id, address, stripe_token, order_details

        order_details: ( json ), example:
                [{"meal_id":1, "quantity":2},
                {"meal_id":2, "quantity":1}]

        returns: {"status":"success"}
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
                meal = Meal.objects.get(id=meal_data['meal_id'])
                quantity = meal_data['quantity']
                OrderDetail.objects.create(
                    order=order, meal=meal,
                    quantity=quantity, sub_total=meal.price * quantity
                )
            return JsonResponse({"status": "success"})


@csrf_exempt
def customer_get_latest_order(request):
    access_token = AccessToken.objects.get(
        token=request.GET.get('access_token'), expires__gt=timezone.now())
    customer = access_token.user.customer
    order = OrderSerializer(Order.objects.filter(
        customer=customer).last()).data
    return JsonResponse({"order": order})


# * ##########
# * RESTAURANT
# * ##########
def restaurant_order_notification(request, last_request_time: str):
    notification = Order.objects.filter(restaurant=request.user.restaurant,
                                        created_at__gt=last_request_time).count()
    return JsonResponse({"notification": notification})


# * ######
# * DRIVER
# * ######

def driver_get_ready_orders(request):
    orders = OrderSerializer(Order.objects.filter(
        status=Order.READY, driver=None).order_by('-id'),
        many=True).data
    return JsonResponse({"orders": orders})


@csrf_exempt
def driver_pick_order(request):
    """ POST params: access_token, order_id """
    if request.method == "POST":
        # Get Token
        access_token = AccessToken.objects.get(
            token=request.POST.get("access_token"), expires__gt=timezone.now())

        # Get Driver
        driver = access_token.user.driver

        # Check if driver can pick 1 order at the same time
        if Order.objects.filter(driver=driver).exclude(status=Order.ONTHEWAY).exists():
            return JsonResponse({"status": "failed",
                                 "error": "You can only pick one order at the same time"})
        try:
            order = Order.objects.get(
                id=request.POST['order_id'],
                driver=None,
                status=Order.READY
            )
            order.driver = driver
            order.status = Order.ONTHEWAY
            order.picked_at = timezone.now()
            order.save()
            return JsonResponse({"status": "success"})
        except Order.DoesNotExist:
            return JsonResponse({"status": "failed", "error": "This order has been picked up by another driver"})


def driver_get_latest_order(request):
    """ GET params : access_token """
    # Get Token
    access_token = AccessToken.objects.get(
        token=request.GET.get("access_token"), expires__gt=timezone.now())
    driver = access_token.user.driver
    order = OrderSerializer(
        Order.objects.filter(driver=driver).order_by("picked_at").last()
    ).data
    return JsonResponse({"order": order})


@csrf_exempt
def driver_complete_order(request):
    """ POST params: access_token, order_id """
    # Get Token
    access_token = AccessToken.objects.get(
        token=request.POST.get("access_token"), expires__gt=timezone.now())
    driver = access_token.user.driver
    order = Order.objects.get(id=request.POST['order_id'], driver=driver)
    order.status = Order.DELIVERED
    order.save()
    return JsonResponse({"status": "success"})


def driver_get_revenue(request):
    return JsonResponse({})

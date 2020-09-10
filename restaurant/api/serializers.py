from rest_framework import serializers

from restaurant.models import Restaurant, Meal, Order, OrderDetail
from user.models import Customer, Driver


class RestaurantSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'phone', 'address', 'logo')

    def get_logo(self, restaurant):
        return get_absolute_uri(self.context, restaurant.logo)


class MealSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Meal
        fields = ('id', 'name', 'short_description', 'image', 'price')

    def get_image(self, meal):
        return get_absolute_uri(self.context, meal.image)


def get_absolute_uri(context, image):
    request = context.get('request')
    return request.build_absolute_uri(image.url)

# * ORDER SERIALIZERS


class OrderCustomerSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="user.get_full_name")

    class Meta:
        model = Customer
        fields = ('id', 'name', 'avatar', 'phone', 'address')


class OrderDriverSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="user.get_full_name")

    class Meta:
        model = Driver
        fields = ('id', 'name', 'avatar', 'phone', 'address')


class OrderRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'phone', 'address')


class OrderMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ('id', 'name', 'price')


class OrderDetailSerializer(serializers.ModelSerializer):
    meal = OrderMealSerializer

    class Meta:
        model = OrderDetail
        fields = ('id', 'meal', 'quantity', 'sub_total')


class OrderSerializer(serializers.ModelSerializer):
    customer = OrderCustomerSerializer()
    driver = OrderDriverSerializer()
    restaurant = OrderRestaurantSerializer()
    order_details = OrderDetailSerializer(many=True)
    status = serializers.ReadOnlyField(source='get_status_display')

    class Meta:
        model = Order
        fields = ('id', 'customer', 'driver', 'restaurant',
                  'order_details', 'status', 'total', 'address')

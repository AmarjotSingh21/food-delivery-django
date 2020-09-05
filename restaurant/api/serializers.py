from rest_framework import serializers

from restaurant.models import Restaurant, Meal


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

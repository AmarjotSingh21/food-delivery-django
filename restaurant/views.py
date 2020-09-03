from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from restaurant.forms import (
    RestaurantForm, UserForm, UserUpdateForm, MealForm)
from .models import Meal, Order


@login_required(login_url='/restaurant/sign-in/')
def home_view(request):
    return redirect('restaurant:order')


def sign_up_view(request):
    user_form = UserForm()
    restaurant_form = RestaurantForm()
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        restaurant_form = RestaurantForm(request.POST, request.FILES)

        if user_form.is_valid() and restaurant_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data)
            new_restaurant = restaurant_form.save(commit=False)
            new_restaurant.user = new_user
            new_restaurant.save()

            login(request, authenticate(username=user_form.cleaned_data['username'],
                                        password=user_form.cleaned_data['password']))
            return redirect('restaurant:home')
    return render(request, 'restaurant/sign_up.html', {
        'user_form': user_form,
        "restaurant_form": restaurant_form
    })


@login_required(login_url='/restaurant/sign-in/')
def account_view(request):
    user_form = UserUpdateForm(instance=request.user)
    restaurant_form = RestaurantForm(instance=request.user.restaurant)

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        restaurant_form = RestaurantForm(
            request.POST, request.FILES, instance=request.user.restaurant)

        if user_form.is_valid() and restaurant_form.is_valid():
            user_form.save()
            restaurant_form.save()
    return render(request, 'restaurant/account.html', {
        "user_form": user_form,
        "restaurant_form": restaurant_form
    })


@login_required(login_url='/restaurant/sign-in/')
def meal_view(request):
    meals = Meal.objects.filter(
        restaurant=request.user.restaurant).order_by('-id')
    print(request.user)
    return render(request, 'restaurant/meal.html', {'meals': meals})


@login_required(login_url='/restaurant/sign-in/')
def add_meal_view(request):
    form = MealForm()

    if request.method == "POST":
        form = MealForm(request.POST, request.FILES)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.restaurant = request.user.restaurant
            meal.save()
            return redirect('restaurant:meal')
    return render(request, 'restaurant/add_meal.html', {'form': form})


@login_required(login_url='/restaurant/sign-in/')
def edit_meal_view(request, meal_id):
    meal = Meal.objects.get(id=meal_id)
    form = MealForm(instance=meal)

    if request.method == "POST":
        form = MealForm(request.POST, request.FILES, instance=meal)
        if form.is_valid():
            meal.save()
            return redirect('restaurant:meal')
    return render(request, 'restaurant/edit_meal.html', {'form': form})


@login_required(login_url='/restaurant/sign-in/')
def order_view(request):
    orders = Order.objects.filter(restaurant=request.user.restaurant)
    return render(request, 'restaurant/order.html', {'orders': orders})


@login_required(login_url='/restaurant/sign-in/')
def report_view(request):
    return render(request, 'restaurant/report.html')

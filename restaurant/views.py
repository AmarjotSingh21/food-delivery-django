from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from restaurant.forms import (RestaurantForm, UserForm, UserUpdateForm)


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
        restaurant_form = RestaurantForm(request.POST, request.FILES, instance=request.user.restaurant)
        
        if user_form.is_valid() and restaurant_form.is_valid():
            user_form.save()
            restaurant_form.save()
    return render(request, 'restaurant/account.html', {
        "user_form": user_form,
        "restaurant_form": restaurant_form
    })


@login_required(login_url='/restaurant/sign-in/')
def meal_view(request):
    return render(request, 'restaurant/meal.html')

@login_required(login_url='/restaurant/sign-in/')
def add_meal_view(request):
    return render(request, 'restaurant/add_meal.html')


@login_required(login_url='/restaurant/sign-in/')
def order_view(request):
    return render(request, 'restaurant/order.html')


@login_required(login_url='/restaurant/sign-in/')
def report_view(request):
    return render(request, 'restaurant/report.html')

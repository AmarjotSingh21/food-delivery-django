from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from restaurant.forms import RestaurantForm, UserForm


@login_required(login_url='/user/sign-in/')
def home_view(request):
    return render(request, 'restaurant/home.html')


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


@login_required(login_url='/user/sign-in/')
def account_view(request):
    return render(request, 'restaurant/account.html')


@login_required(login_url='/user/sign-in/')
def meal_view(request):
    return render(request, 'restaurant/meal.html')


@login_required(login_url='/user/sign-in/')
def order_view(request):
    return render(request, 'restaurant/order.html')


@login_required(login_url='/user/sign-in/')
def report_view(request):
    return render(request, 'restaurant/report.html')

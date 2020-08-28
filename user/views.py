from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .forms import UserForm
from restaurant.forms import RestaurantForm


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
    return render(request, 'user/sign_up.html', {
        'user_form': user_form,
        "restaurant_form": restaurant_form
    })

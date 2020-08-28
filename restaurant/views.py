from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import UserForm, RestaurantForm


@login_required(login_url='/user/sign-in/')
def restaurant_home(request):
    return render(request, 'restaurant/home.html')



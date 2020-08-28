from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required(login_url='/user/sign-in/')
def home_view(request):
    return render(request, 'restaurant/home.html')


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

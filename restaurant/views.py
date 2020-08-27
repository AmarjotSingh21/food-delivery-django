from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/restaurant/sign-in/')
def restaurant_home(request):
    return render(request, 'restaurant/home.html')


def restaurant_sign_up(request):
    return render(request, 'restaurant/sign_up.html')

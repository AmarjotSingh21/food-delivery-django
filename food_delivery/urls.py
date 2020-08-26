from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('restaurant/sign-in/', auth_views.LoginView.as_view(
        template_name='restaurant/sign_in.html'), name='restaurant-sign-in'),
    path('restaurant/sign-out/', auth_views.LogoutView.as_view(
        template_name='restaurant/sign_out.html',), name='restaurant-sign-out'),
    path('restaurant/', include('restaurant.urls')),
]

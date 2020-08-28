from django.db import models
from django.contrib.auth.models import User


class UserFields(models.Model):
    avatar = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)

    class Meta:
        abstract = True


class Customer(UserFields):
    user = models.OneToOneField(
        User,  on_delete=models.CASCADE, related_name='customer')

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return self.user.get_full_name()


class Driver(UserFields):
    user = models.OneToOneField(
        User,  on_delete=models.CASCADE, related_name='driver')

    class Meta:
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'

    def __str__(self):
        return self.user.get_full_name()

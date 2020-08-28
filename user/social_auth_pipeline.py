from .models import Customer, Driver


def create_user_by_type(backend, user, strategy, response, *args, **kwargs):
    if backend.name == 'facebook':
        avatar = f'https://graph.facebook.com/{ response["id"] }/picture?type=large'

    request = strategy.request
    if (request.POST['user_type'] == "driver" and
            not Driver.objects.filter(user=user).exists()):
        Driver.objects.create(user=user, avatar=avatar)
    elif not Customer.objects.filter(user=user, avatar=avatar).exists():
        Customer.objects.create(user=user, avatar=avatar)

from django.contrib.auth.hashers import make_password


def custom_asher_asham(password):
    reversed_password = password[::-1] + "s@lt"
    return make_password(reversed_password)

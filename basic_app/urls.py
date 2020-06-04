"""This file is for inter-app routing"""
from django.urls import path
from . import views

# TEMPLATE TAGGING
app_name = 'basic_app'

# interapp routing
urlpatterns = [
    path('', views.index, name="index"),
    path('register', views.register, name="register"),
    path('login', views.user_login, name="login"),
    path('logout', views.user_logout, name="logout"),
    path('special', views.special, name="special"),
]
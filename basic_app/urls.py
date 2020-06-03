"""This file is for inter-app routing"""
from django.urls import path
from . import views

# TEMPLATE TAGGING
app_name = 'basic_app'

# interapp routing
urlpatterns = [
    path('register', views.register, name="register")
]
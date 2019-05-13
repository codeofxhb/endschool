from django.urls import path
from . import views

urlpatterns = [
    path('give_like', views.give_like, name='give_like'),
]
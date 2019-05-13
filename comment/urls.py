from django.urls import path
from . import views

urlpatterns = [
    path('comment_add', views.comment_add, name='comment_add'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('blog_list', views.blog_list, name="blog_list"),
    path('<int:blog_pk>', views.blog_detail, name="blog_detail"),
    path('blog_type/<int:blogtype_id>', views.blog_type, name="blog_type"),
    path('blog_times/<int:blog_year>/<int:blog_month>/<int:blog_day>', views.blog_times, name="blog_times"),
]

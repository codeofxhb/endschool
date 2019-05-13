from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name="login"),
    path('login_for_medal', views.login_for_medal, name="login_for_medal"),
    path('register', views.register, name="register"),
    path('login_out', views.login_out, name="login_out"),
    path('user_info', views.user_info, name="user_info"),
    path('change_niname', views.change_niname, name="change_niname"),
    path('bind_email', views.bind_email, name="bind_email"),
    path('send_verification_mail', views.send_verification_mail, name="send_verification_mail"),
    path('change_password', views.change_password, name="change_password"),
    path('find_password', views.find_password, name="find_password"),
]

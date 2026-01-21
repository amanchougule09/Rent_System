from django.urls import path
from .views import login_view, register_view ,change_password, logout_view  
from .views import root_redirect
from . import views

app_name = "accounts"

urlpatterns = [
    path("",root_redirect),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("change_password/", views.change_password, name="change_password"),
    path("logout/", views.logout_view, name="logout"),
]

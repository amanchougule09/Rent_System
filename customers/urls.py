from django.urls import path
from . import views

app_name = "customers"

urlpatterns = [
    path("", views.room_list, name="room_list"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("rooms/<int:id>/", views.room_detail, name="room_detail"),
]

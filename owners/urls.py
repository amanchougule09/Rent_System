from django.urls import path
from . import views

app_name = "owners"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),

    path("tenants/", views.tenant_list, name="tenant_list"),
    path("tenants/add/", views.add_tenant, name="add_tenant"),
    path("tenants/<int:id>/", views.tenant_detail, name="tenant_detail"),
    path("tenants/delete/<int:id>/", views.delete_tenant, name="delete_tenant"),

    path("rooms/", views.room_list, name="room_list"),
    path("rooms/add/", views.add_room, name="add_room"),
    path("rooms/<int:id>/", views.room_detail, name="room_detail"),
    path("rooms/<int:room_id>/edit/", views.edit_room, name="edit_room"),
    path("rooms/<int:room_id>/delete/", views.delete_room, name="delete_room"),

    path("rooms/<int:room_id>/assign-tenant/", views.assign_tenant, name="assign_tenant"),
    path("rooms/<int:room_id>/vacate/", views.vacate_room, name="vacate_room"),

    path("profile/", views.profile, name="profile"),
    path("bookings/", views.bookings_list, name="bookings_list"),
    path("tenants/<int:id>/paid/", views.mark_paid, name="mark_paid"),
    path("tenants/<int:id>/unpaid/", views.mark_unpaid, name="mark_unpaid"),
]

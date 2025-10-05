from django.urls import path
from .views import views

urlpatterns = [
    # rooms
    path("rooms/add", views.add_room, name="add_room"),
    path("rooms/delete/<int:room_id>", views.delete_room, name="delete room"),
    path("rooms/list", views.get_room_list, name="room_list"),

    # bookings
    path("bookings/add", views.add_booking, name="add_booking"),
    path("bookings/delete/<int:booking_id>", views.delete_booking, name="delete_booking"),
    path("bookings/list", views.get_booking_list, name="booking_list"),
]
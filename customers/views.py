from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from datetime import datetime

from rooms.models import Room
from rent.models import Booking


def dashboard(request):
    return render(request, "customers/dashboard.html")


def room_list(request):
    rooms = Room.objects.filter(is_available=True)
    return render(request, "customers/room_list.html", {"rooms": rooms})


def room_detail(request, id):
    room = get_object_or_404(Room, id=id)
    errors = {}

    if request.method == "POST":
        start = request.POST.get("start_date")
        end = request.POST.get("end_date")
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()

        try:
            start_date = datetime.strptime(start, "%Y-%m-%d").date()
            end_date = datetime.strptime(end, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            errors["date"] = "Invalid dates"

        if not name:
            errors["name"] = "Name required"
        if not email:
            errors["email"] = "Email required"

        if not errors:
            booking = Booking.objects.create(
                room=room,
                start_date=start_date,
                end_date=end_date,
                customer_name=name,
                customer_email=email,
                customer_phone=phone,
                status="pending",
            )

            # Send simple confirmation (console/email backend)
            send_mail(
                "Booking request received",
                f"Thank you {name}. Your booking request (id: {booking.id}) for {room.title} has been received.",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=True,
            )

            messages.success(request, "Booking request received. We sent a confirmation email.")
            return redirect("customers:room_detail", id=room.id)

    return render(request, "customers/room_detail.html", {"room": room, "errors": errors})


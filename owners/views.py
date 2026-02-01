from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils.timezone import now

from accounts.decorators import login_required, owner_required
from owners.models import Owner
from tenants.models import Tenant
from rooms.models import Room
from rent.models import Booking


# ------------------------------------
# HELPER
# ------------------------------------
def get_owner(request):
    return get_object_or_404(Owner, user_id=request.session["user_id"])


# ------------------------------------
# OWNER DASHBOARD
# ------------------------------------
@login_required
@owner_required
def dashboard(request):
    owner = get_owner(request)
    tenants = Tenant.objects.filter(owner=owner)
    rooms = Room.objects.filter(owner=owner)
    paid_tenants = tenants.filter(paid=True)
    
    # Calculate total rent collected
    total_rent_collected = sum([t.amount for t in paid_tenants])
    
    # Calculate occupancy rate
    total_rooms = rooms.count()
    occupied_rooms = rooms.filter(is_available=False).count()
    occupancy_rate = (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0
    
    # Calculate upcoming rent due
    upcoming_rent = sum([t.amount for t in tenants.filter(paid=False)])

    context = {
        "total": tenants.count(),
        "paid": tenants.filter(paid=True).count(),
        "unpaid": tenants.filter(paid=False).count(),
        "overdue": tenants.filter(due_date__lt=date.today(), paid=False).count(),
        "next_due": tenants.order_by("due_date").first(),
        "total_rent_collected": total_rent_collected,
        "occupancy_rate": round(occupancy_rate),
        "upcoming_rent": upcoming_rent,
        "recent_tenants": tenants.order_by("-id")[:5],
    }
    return render(request, "owners/dashboard.html", context)


# ------------------------------------
# TENANTS
# ------------------------------------
@login_required
@owner_required
def tenant_list(request):
    owner = get_owner(request)
    tenants = Tenant.objects.filter(owner=owner)
    return render(request, "owners/tenant_list.html", {"tenants": tenants})


@login_required
@owner_required
def add_tenant(request):
    owner = get_owner(request)
    errors = {}
    form_data = request.POST.dict()

    if request.method == "POST":
        name = request.POST.get("name", "").strip().title()
        mobile = request.POST.get("mobile", "").strip()
        amount_raw = request.POST.get("amount", "").strip()
        due_type = request.POST.get("due_type")
        due_date_raw = request.POST.get("due_date")
        deposit_raw = request.POST.get("security_deposit", "0")

        if not name:
            errors["name"] = "Name required"

        if not mobile.isdigit() or len(mobile) != 10:
            errors["mobile"] = "Invalid mobile number"

        if Tenant.objects.filter(owner=owner, user__mobile=mobile).exists():
            errors["mobile"] = "Tenant already exists"

        try:
            amount = Decimal(amount_raw)
            if amount <= 0:
                raise ValueError
        except:
            errors["amount"] = "Invalid amount"

        try:
            deposit = Decimal(deposit_raw)
            if deposit < 0:
                raise ValueError
        except:
            errors["security_deposit"] = "Invalid deposit"

        if due_type == "fixed" and not due_date_raw:
            errors["due_date"] = "Due date required"

        if errors:
            return render(request, "owners/add_tenant.html", {
                "errors": errors,
                "form_data": form_data
            })

        if due_type == "fixed":
            due_date = datetime.strptime(due_date_raw, "%Y-%m-%d").date()
        else:
            due_date = None

        from accounts.models import UserProfile
        tenant_user, created = UserProfile.objects.get_or_create(
            mobile=mobile,
            defaults={"role": "tenant"}
        )
        if created:
            tenant_user.set_password(mobile[-4:])
            tenant_user.save()

        Tenant.objects.create(
            user=tenant_user,
            owner=owner,
            name=name,
            amount=amount,
            due_type=due_type,
            due_date=due_date,
            security_deposit=deposit
        )

        return redirect("owners:tenant_list")

    return render(request, "owners/add_tenant.html", {"errors": {}, "form_data": {}})


@login_required
@owner_required
def tenant_detail(request, id):
    owner = get_owner(request)
    tenant = get_object_or_404(Tenant, id=id, owner=owner)
    return render(request, "owners/tenant_detail.html", {"tenant": tenant})


@login_required
@owner_required
def delete_tenant(request, id):
    owner = get_owner(request)
    tenant = get_object_or_404(Tenant, id=id, owner=owner)
    tenant.delete()
    return redirect("owners:tenant_list")


# ------------------------------------
# ROOMS
# ------------------------------------
@login_required
@owner_required
def room_list(request):
    owner = get_owner(request)
    rooms = Room.objects.filter(owner=owner)
    
    # Handle search functionality
    search = request.GET.get('search', '').strip()
    if search:
        rooms = rooms.filter(title__icontains=search) | rooms.filter(room_number__icontains=search) | rooms.filter(location__icontains=search)
    
    return render(request, "owners/room_list.html", {"rooms": rooms, "search": search})


@login_required
@owner_required
def add_room(request):
    owner = get_owner(request)
    errors = {}
    form_data = request.POST.dict()

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        room_number = request.POST.get("room_number", "").strip()
        rent_raw = request.POST.get("rent_amount", "").strip()
        location = request.POST.get("location", "").strip()
        description = request.POST.get("description", "").strip()
        image = request.FILES.get("image")

        if not title:
            errors["title"] = "Title required"
        if not room_number:
            errors["room_number"] = "Room number required"
        if not rent_raw.isdigit() or int(rent_raw) <= 0:
            errors["rent_amount"] = "Invalid rent"
        if not location:
            errors["location"] = "Location required"
        if Room.objects.filter(owner=owner, room_number=room_number).exists():
            errors["room_number"] = "Room already exists"

        if errors:
            return render(request, "owners/add_room.html", {
                "errors": errors,
                "form_data": form_data
            })

        Room.objects.create(
            owner=owner,
            title=title,
            room_number=room_number,
            rent_amount=int(rent_raw),
            location=location,
            description=description,
            image=image
        )
        return redirect("owners:room_list")

    return render(request, "owners/add_room.html", {"errors": {}, "form_data": {}})


@login_required
@owner_required
def room_detail(request, id):
    owner = get_owner(request)
    room = get_object_or_404(Room, id=id, owner=owner)
    return render(request, "owners/room_detail.html", {"room": room})


@login_required
@owner_required
def edit_room(request, room_id):
    owner = get_owner(request)
    room = get_object_or_404(Room, id=room_id, owner=owner)

    if request.method == "POST":
        room.title = request.POST.get("title")
        room.room_number = request.POST.get("room_number")
        room.rent_amount = request.POST.get("rent_amount")
        room.location = request.POST.get("location")
        room.description = request.POST.get("description")
        room.is_available = request.POST.get("is_available") == "on"

        if request.FILES.get("image"):
            room.image = request.FILES["image"]

        room.save()
        return redirect("owners:room_detail", room.id)

    return render(request, "owners/edit_room.html", {"room": room})


@require_POST
@login_required
@owner_required
def delete_room(request, room_id):
    owner = get_owner(request)
    room = get_object_or_404(Room, id=room_id, owner=owner)
    Tenant.objects.filter(room=room).update(room=None)
    room.delete()
    return redirect("owners:room_list")


# ------------------------------------
# ASSIGN / VACATE
# ------------------------------------
@login_required
@owner_required
def assign_tenant(request, room_id):
    owner = get_owner(request)
    room = get_object_or_404(Room, id=room_id, owner=owner)
    tenants = Tenant.objects.filter(owner=owner, room__isnull=True)

    if request.method == "POST":
        tenant = get_object_or_404(Tenant, id=request.POST.get("tenant"), owner=owner)
        tenant.room = room
        tenant.save()

        room.is_available = False
        room.save()

        return redirect("owners:room_detail", room.id)

    return render(request, "owners/assign_tenant.html", {"room": room, "tenants": tenants})


@require_POST
@login_required
@owner_required
def vacate_room(request, room_id):
    owner = get_owner(request)
    room = get_object_or_404(Room, id=room_id, owner=owner)
    Tenant.objects.filter(room=room).update(room=None)
    room.is_available = True
    room.save()
    return redirect("owners:room_detail", room.id)


# ------------------------------------
# BOOKINGS
# ------------------------------------
@login_required
@owner_required
def bookings_list(request):
    owner = get_owner(request)
    bookings = Booking.objects.filter(room__owner=owner).order_by("-created_at")
    return render(request, "owners/bookings_list.html", {"bookings": bookings})


# ------------------------------------
# MANAGEMENT
# ------------------------------------
@login_required
@owner_required
def management(request):
    owner = get_owner(request)
    rooms = Room.objects.filter(owner=owner)
    tenants = Tenant.objects.filter(owner=owner)
    
    context = {
        "total_rooms": rooms.count(),
        "available_rooms": rooms.filter(is_available=True).count(),
        "occupied_rooms": rooms.filter(is_available=False).count(),
        "total_tenants": tenants.count(),
        "paid_tenants": tenants.filter(paid=True).count(),
        "unpaid_tenants": tenants.filter(paid=False).count(),
    }
    return render(request, "owners/management.html", context)


# ------------------------------------
# PROFILE
# ------------------------------------
@login_required
@owner_required
def profile(request):
    try:
        owner = Owner.objects.get(user_id=request.session["user_id"])
    except Owner.DoesNotExist:
        request.session.flush()
        return redirect("accounts:login")

    return render(request, "owners/profile.html", {"owner": owner})


# ------------------------------------
# PAYMENT STATUS
# ------------------------------------
@require_POST
@login_required
@owner_required
def mark_paid(request, id):
    owner = get_owner(request)
    tenant = get_object_or_404(Tenant, id=id, owner=owner)
    tenant.paid = True
    tenant.payment_date = now().date()
    tenant.save()
    return redirect("owners:tenant_detail", tenant.id)


@require_POST
@login_required
@owner_required
def mark_unpaid(request, id):
    owner = get_owner(request)
    tenant = get_object_or_404(Tenant, id=id, owner=owner)
    tenant.paid = False
    tenant.payment_date = None
    tenant.save()
    return redirect("owners:tenant_detail", tenant.id)

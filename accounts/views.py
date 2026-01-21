from django.shortcuts import render, redirect
from .models import UserProfile
from tenants.models import Tenant
from owners.models import Owner


# ------------------------------------
# LOGIN
# ------------------------------------
def login_view(request):
    # 🚫 Block login page if already logged in
    if request.session.get("user_id"):
        role = request.session.get("role")
        if role == "owner":
            return redirect("owners:dashboard")
        elif role == "tenant":
            return redirect("tenants:dashboard")
        else:
            return redirect("customers:room_list")

    error = None

    if request.method == "POST":
        mobile = request.POST.get("mobile", "").strip()
        password = request.POST.get("password", "").strip()

        try:
            user = UserProfile.objects.get(mobile=mobile)

            if not user.check_password(password):
                error = "Incorrect password"
            else:
                # 🔐 Reset old session & create fresh one
                request.session.flush()
                request.session["user_id"] = user.id
                request.session["mobile"] = user.mobile
                request.session["role"] = user.role

                # ⏱️ Auto logout after 1 hour (professional touch)
                request.session.set_expiry(60 * 60)

                if user.role == "owner":
                    return redirect("owners:dashboard")
                elif user.role == "tenant":
                    return redirect("tenants:dashboard")
                else:
                    return redirect("customers:room_list")

        except UserProfile.DoesNotExist:
            error = "Account does not exist"

    return render(request, "accounts/login.html", {"error": error})


# ------------------------------------
# REGISTER (OWNER ONLY)
# ------------------------------------
def register_view(request):
    # 🚫 Logged-in users cannot register again
    if request.session.get("user_id"):
        return redirect("owners:dashboard")

    error = None

    if request.method == "POST":
        mobile = request.POST.get("mobile", "").strip()
        password = request.POST.get("password", "").strip()

        # validations
        if not mobile.isdigit() or len(mobile) != 10:
            error = "Enter a valid 10-digit mobile number"
        elif len(password) < 4:
            error = "Password must be at least 4 characters"
        elif UserProfile.objects.filter(mobile=mobile).exists():
            error = "Mobile number already registered"
        else:
            # create user profile
            user = UserProfile(
                mobile=mobile,
                role="owner"
            )
            user.set_password(password)
            user.save()

            # ✅ Create Owner profile
            Owner.objects.get_or_create(user=user, name="")

            # auto login
            request.session.flush()
            request.session["user_id"] = user.id
            request.session["mobile"] = user.mobile
            request.session["role"] = user.role
            request.session.set_expiry(60 * 60)

            return redirect("owners:dashboard")

    return render(request, "accounts/register.html", {"error": error})


# ------------------------------------
# CHANGE PASSWORD
# ------------------------------------
def change_password(request):
    if not request.session.get("mobile"):
        return redirect("accounts:login")

    try:
        user = UserProfile.objects.get(mobile=request.session["mobile"])
    except UserProfile.DoesNotExist:
        request.session.flush()
        return redirect("accounts:login")

    error = None
    success = None

    if request.method == "POST":
        old = request.POST.get("old_password")
        new = request.POST.get("new_password")
        confirm = request.POST.get("confirm_password")

        if not user.check_password(old):
            error = "Old password incorrect"
        elif new != confirm:
            error = "Passwords do not match"
        elif len(new) < 4:
            error = "Password must be at least 4 characters"
        else:
            user.set_password(new)
            success = "Password changed successfully"

    return render(request, "accounts/change_password.html", {
        "error": error,
        "success": success
    })


# -----------------------------------------------
# LOGOUT
# -----------------------------------------------
def logout_view(request):
    request.session.flush()
    return redirect("customers:room_list")


# -----------------------------------------------
# ROOT REDIRECT
# -----------------------------------------------
def root_redirect(request):
    role = request.session.get("role")
    user_id = request.session.get("user_id")

    # 🌍 Public users → public room list
    if not role or not user_id:
        return redirect("customers:room_list")

    if role == "owner":
        try:
            Owner.objects.get(user_id=user_id)
            return redirect("owners:dashboard")
        except Owner.DoesNotExist:
            request.session.flush()

    elif role == "tenant":
        try:
            Tenant.objects.get(user_id=user_id)
            return redirect("tenants:dashboard")
        except Tenant.DoesNotExist:
            request.session.flush()

    return redirect("customers:room_list")

# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse
# from .models import Tenant
# from datetime import datetime, date, timedelta
# from django.contrib import messages
# from decimal import Decimal, InvalidOperation

# def home(request):
#     owner_mobile = request.session.get("mobile")

#     # If not logged in → redirect
#     if not owner_mobile:
#         return redirect("login")

#     tenants = Tenant.objects.filter(owner_mobile=owner_mobile)

#     total = tenants.count()
#     paid = tenants.filter(paid=True).count()
#     unpaid = tenants.filter(paid=False).count()
#     overdue = tenants.filter(due_date__lt=date.today(), paid=False).count()

#     # Next due tenant
#     next_due = tenants.order_by("due_date").first()

#     context = {
#         "total": total,
#         "paid": paid,
#         "unpaid": unpaid,
#         "overdue": overdue,
#         "next_due": next_due,
#     }

#     return render(request, "rent/home.html", context)


# def tenant(request):
#     owner_mobile = request.session.get("mobile")
#     tenants = Tenant.objects.filter(owner_mobile=owner_mobile)
       
#     return render(request, "rent/tenant.html", {"tenants": tenants})

# def chat(request):
#     # static placeholder - later you can wire chat backend or messages
#     messages = [
#         {"from": "Owner", "text": "Welcome!"},
#         {"from": "Tenant", "text": "Hi, I have a query."},
#     ]
#     return render(request, "rent/chat.html", {"messages": messages})

# def profile(request):
#     user = {"name": "Aman", "email": "aman@example.com"}
#     return render(request, "rent/profile.html", {"user": user})

# def add_tenant(request):
#     owner_mobile = request.session.get("mobile")
#     form_data = request.POST.dict()
#     errors = {}

#     if request.method == "POST":
#         name = request.POST.get("name", "").strip().title()
#         mobile = request.POST.get("mobile", "").strip()
#         amount = request.POST.get("amount", "").strip()
#         due_type = request.POST.get("due_type")
#         due_date = request.POST.get("due_date")

#         security_deposit_raw = request.POST.get("security_deposit", "").strip()
#         room_number = request.POST.get("room_number", "").strip()

#         # NAME
#         if not name:
#             errors["name"] = "Name is required."

#         # MOBILE validations
#         if owner_mobile == mobile:
#             errors["mobile"] = "Owner mobile and tenant mobile cannot be same."
#         elif Tenant.objects.filter(owner_mobile=owner_mobile, mobile=mobile).exists():
#             errors["mobile"] = "This tenant already exists."
#         elif not mobile.isdigit() or len(mobile) != 10 or mobile[0] not in "6789":
#             errors["mobile"] = "Enter a valid 10-digit Indian mobile number."
#         elif mobile in ["0000000000", "9999999999", "1234567890"]:
#             errors["mobile"] = "Enter a valid Indian mobile number."

#         # AMOUNT
#         if not amount.isdigit() or int(amount) <= 0:
#             errors["amount"] = "Enter a valid amount."

#         # SECURITY DEPOSIT validation
#         if security_deposit_raw == "":
#             # treat empty as zero
#             security_deposit_raw = "0"
#         try:
#             # allow decimals
#             security_deposit = Decimal(security_deposit_raw)
#             if security_deposit < 0:
#                 errors["security_deposit"] = "Security deposit cannot be negative."
#         except (InvalidOperation, ValueError):
#             errors["security_deposit"] = "Enter a valid deposit amount (e.g., 5000 or 2500.50)."

#         # ROOM NUMBER (optional) — basic sanitization
#         if len(room_number) > 50:
#             errors["room_number"] = "Room number is too long."

#         # DUE TYPE
#         if due_type not in ["fixed", "cycle"]:
#             errors["due_type"] = "Please select a valid due type."

#         # DUE DATE if fixed
#         if due_type == "fixed":
#             if not due_date:
#                 errors["due_date"] = "Please select a due date."

#         # If errors exist → re-render with messages
#         if errors:
#             form_data["security_deposit"] = security_deposit_raw
#             form_data["room_number"] = room_number
#             return render(request, "rent/add_tenant.html", {
#                 "errors": errors,
#                 "form_data": form_data
#             })

#         # Save tenant
#         if due_type == "fixed":
#             try:
#                 due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
#             except:
#                 errors["due_date"] = "Invalid date format."
#                 form_data["security_deposit"] = security_deposit_raw
#                 form_data["room_number"] = room_number
#                 return render(request, "rent/add_tenant.html", {
#                     "errors": errors,
#                     "form_data": form_data
#                 })
#         else:
#             due_date = None

#         Tenant.objects.create(
#             owner_mobile=owner_mobile,
#             name=name,
#             mobile=mobile,
#             amount=amount,
#             due_type=due_type,
#             due_date=due_date,
#             security_deposit=security_deposit,
#             room_number=room_number

#         )

#         return redirect("tenant")

#     return render(request, "rent/add_tenant.html", {
#         "form_data": {},
#         "errors": {}
#     })


# def tenant_detail(request, id):
#     owner_mobile = request.session.get("mobile")
#     tenant = get_object_or_404(Tenant, id=id, owner_mobile=owner_mobile)

#     return render(request, "rent/tenant_detail.html", {"tenant": tenant})



# from django.shortcuts import get_object_or_404

# def delete_tenant(request, tenant_id):
#     tenant = get_object_or_404(Tenant, id=tenant_id)
#     tenant.delete()
#     return redirect('tenant')

# def login_page(request):
#     error = None
#     if request.method == "POST":
#         mobile = request.POST.get("mobile")
#         if not mobile.isdigit() or len(mobile) != 10 or mobile[0] not in "6789":
#             error = "Enter a valid 10-digit Indian mobile number"
#         else:
#             # Save mobile in session and redirect to home
#             request.session["mobile"] = mobile
#             return redirect("home")

#     return render(request, "rent/login.html", {"error": error})

# def logout_page(request):
#     if "mobile" in request.session:
#         del request.session["mobile"]
#     return redirect("login")
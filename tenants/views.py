from django.shortcuts import render, redirect, get_object_or_404
from tenants.models import Tenant
from accounts.decorators import login_required, tenant_required

@login_required
@tenant_required
@login_required
@tenant_required
def dashboard(request):
    tenant = get_object_or_404(
        Tenant,
        user_id=request.session.get("user_id")
    )
    return render(request, "tenants/dashboard.html", {"tenant": tenant})

@login_required
@tenant_required
def profile(request):
    tenant = get_object_or_404(
        Tenant,
        user_id=request.session.get("user_id")
    )
    return render(request, "tenants/profile.html", {"tenant": tenant})
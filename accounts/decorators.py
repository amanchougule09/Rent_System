from django.shortcuts import redirect

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("user_id"):
            return redirect("accounts:login")
        return view_func(request, *args, **kwargs)
    return wrapper


def owner_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("user_id"):
            return redirect("accounts:login")
        if request.session.get("role") != "owner":
            return redirect("accounts:login")
        return view_func(request, *args, **kwargs)
    return wrapper


def tenant_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("user_id"):
            return redirect("accounts:login")
        if request.session.get("role") != "tenant":
            return redirect("accounts:login")
        return view_func(request, *args, **kwargs)
    return wrapper

from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')  # Redirect if not logged in

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name  

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to view this page", status=403)

        return wrapper_func
    return decorator



def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)  # Allow superusers

        if request.user.groups.exists():
            user_groups = set(request.user.groups.values_list('name', flat=True))
            
            if 'admin' in user_groups:
                return view_func(request, *args, **kwargs)  # Allow admin users
            
            if 'customer' in user_groups:
                return redirect('userPage')  # Redirect customers

        # 🚨 If the user has no group, return forbidden response
        return HttpResponse("Forbidden: You don't have access.", status=403)

    return wrapper_func

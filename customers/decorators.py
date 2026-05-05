from django.http import HttpResponseForbidden
from functools import wraps

def role_required(role_flag):
    """
    Restricts view access to users with a specific role flag.
    Usage: @role_required('is_manager')
    Returns 403 Forbidden if the authenticated user lacks the required role.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = request.user
            if not user or not getattr(user, 'is_authenticated', False):
                from django.shortcuts import redirect
                return redirect('login')
            if not getattr(user, role_flag, False):
                return HttpResponseForbidden(
                    "Access denied: you do not have permission to view this page."
                )
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

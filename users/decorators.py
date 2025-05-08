from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied

def role_required(*roles):
    """
    Decorator to restrict access based on user roles.
    Accepts one or more role names.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())

            if request.user.role not in roles:
                return redirect('access_denied')  # Or render a nice 'no access' template

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

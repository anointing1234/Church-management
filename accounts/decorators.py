from django.shortcuts import redirect
from functools import wraps

def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.is_superuser or request.user.role in allowed_roles:
                    return view_func(request, *args, **kwargs)
            return redirect('no_permission')  # Or return a custom 403 page
        return _wrapped_view
    return decorator

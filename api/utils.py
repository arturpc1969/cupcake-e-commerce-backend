from functools import wraps

from django.http import HttpResponse


# --- Decorator to require the user to be staff ---
def staff_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user = request.auth
        if not user or not user.is_staff:
            return HttpResponse(status=403)
        return func(request, *args, **kwargs)
    return wrapper

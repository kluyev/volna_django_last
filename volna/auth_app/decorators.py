from django.http import HttpResponseForbidden
from functools import wraps

def staff_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role not in ['staff', 'admin']:
            return HttpResponseForbidden("Доступ запрещен")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
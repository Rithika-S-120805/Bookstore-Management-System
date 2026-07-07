from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def admin_required(view_func):
    @wraps(view_func)
    @login_required(login_url='login')
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return render(request, '403.html', status=403)
        return view_func(request, *args, **kwargs)

    return _wrapped_view
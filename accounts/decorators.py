import functools
from django.shortcuts import redirect

def two_factor_required(view_func, redirect_url="accounts:two_factor"):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_two_factor.verify:
            return view_func(request, *args, **kwargs)
        return redirect(redirect_url)
    return wrapper
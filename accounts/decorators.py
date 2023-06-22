import functools
from django.shortcuts import redirect

def two_factor_required(view_func, redirect_url="accounts:two_factor"):
    """
        this decorator ensures that a user is not logged in,
        if a user is logged in, the user will get redirected to
        the url whose view name was passed to the redirect_url parameter
    """

    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_two_factor.verify:
            return view_func(request, *args, **kwargs)
        # messages.add_message(request, messages.INFO, 'You need to be logged out')
        return redirect(redirect_url)
    return wrapper
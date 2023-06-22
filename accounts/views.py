from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model, logout
from .models import TwoFactorAuth
from .forms import TwoFactorForm, MyAuthenticationForm
from django.contrib.auth.decorators import login_required
from .decorators import two_factor_required
from django.contrib import messages
User = get_user_model()


def my_login_view(request):
    if request.method == "POST":
        form = MyAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                TwoFactorAuth.objects.get_or_create(user=user)
                send_mail(
                    "Kodi me 6 shifra i gjeruar",
                    f"kodi: {user.user_two_factor.code}.",
                    "from@example.com",
                    ["to@example.com"],
                    fail_silently=False,
                )
                login(request, user)
                return redirect("accounts:two_factor")
    else:
        form = MyAuthenticationForm()
    return render(request, 'login.html', {"form": form})


@login_required
@two_factor_required
def home(request):
    return render(request, 'home.html')


@login_required
def two_factor_view(request):
    expired = False
    get_twofactor = get_object_or_404(TwoFactorAuth, user_id=request.user.id)
    if request.method == "POST":
        form = TwoFactorForm(data=request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if get_twofactor.code == code:
                if get_twofactor.check_expires_code < 2:
                    get_twofactor.verify = True
                    get_twofactor.save(update_fields=["verify"])
                    return redirect("accounts:home")
                else:
                    expired = True
                    messages.add_message(request, messages.WARNING, "Your code has expired, please request another one.", extra_tags="warning")
            else:
                messages.add_message(request, messages.ERROR, "The code you entered is incorrect.", extra_tags="danger")
    else:
        form = TwoFactorForm()
    return render(request, 'two_factor.html', {'form': form, "expired": expired})

@login_required
def generate_new_code(request):
    TwoFactorAuth.objects.update_or_create(user=request.user)
    send_mail(
        "Kodi me 6 shifra i gjeruar",
        f"kodi: {request.user.user_two_factor.code}.",
        "from@example.com",
        ["to@example.com"],
        fail_silently=False,
    )
    return redirect("accounts:two_factor")

@login_required
def logout_view(request):
    get_twofactor = get_object_or_404(TwoFactorAuth, user_id=request.user.id)
    get_twofactor.delete()
    logout(request)
    return redirect("accounts:login")

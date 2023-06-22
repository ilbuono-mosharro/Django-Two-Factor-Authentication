from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('',  views.home, name="home"),
    path('login/', views.my_login_view, name="login"),
    path("verify/two-factor/", views.two_factor_view, name="two_factor"),
    path('log-out/', views.logout_view, name="logout_view"),
    path('generate_new_code/', views.generate_new_code, name="generate_new_code"),
]
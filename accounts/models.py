from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
import random
import datetime
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
# Create your models here.

def generate_code():
    code = random.randint(100000, 999999)
    try:
        TwoFactorAuth.objects.get(code=code)
        return generate_code()
    except TwoFactorAuth.DoesNotExist:
        return code

class MyUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

class MyUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class TwoFactorAuth(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name="user_two_factor")
    code = models.CharField(max_length=6)
    expires = models.DateTimeField(auto_now=True)
    verify = models.BooleanField(default=False)


    def save(self, update_fields=None, *args, **kwargs):
        if not self.code or update_fields:
            self.code = generate_code()
        super().save(*args, **kwargs)

    @property
    def check_expires_code(self):
        minutes_difference = datetime.datetime.now().minute - self.expires.minute
        return minutes_difference

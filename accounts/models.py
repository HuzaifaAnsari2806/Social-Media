from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser


from utilities.models import BaseModel
from .managers import UserManager


class User(AbstractBaseUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_on = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self) -> str:
        return self.email


class Profile(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150)
    profile_pic = models.ImageField(upload_to="user/", null=True, blank=True)
    mobile_number = models.CharField(max_length=10, unique=True, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, default="India")
    twitter_url = models.URLField(max_length=255, blank=True, null=True)
    facebook_url = models.URLField(max_length=255, blank=True, null=True)
    linkdln_url = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username

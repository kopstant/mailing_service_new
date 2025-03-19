from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'blank': True, 'null': True}


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=254, verbose_name="email")
    avatar = models.ImageField(upload_to="users/avatars/", verbose_name="avatar", **NULLABLE)
    phone_number = models.CharField(max_length=11, unique=True, verbose_name="phone number", **NULLABLE)
    country = models.CharField(max_length=50, verbose_name="country", **NULLABLE)
    token = models.CharField(max_length=100, verbose_name="token", **NULLABLE)
    is_blocked = models.BooleanField(default=False, verbose_name="is blocked")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        permissions = []

    def __str__(self):
        return self.email

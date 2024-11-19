from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, username=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, username, **extra_fields)

class User(AbstractBaseUser):
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField(unique=True, blank=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["email", "username", "password"]

    objects = UserManager()
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class UserRole(models.TextChoices):
    ADMIN = "admin", "Admin"
    DRIVER = "driver", "Driver"
    RIDER = "rider", "Rider"


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email address is required.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id_user = models.BigAutoField(primary_key=True)
    role = models.CharField(max_length=20, choices=UserRole.choices, db_index=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True, blank=False)
    phone_number = models.CharField(max_length=15)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("first_name", "last_name")

    class Meta:
        db_table = "user"

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"

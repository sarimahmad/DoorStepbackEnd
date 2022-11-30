from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone


from django.contrib.auth.models import (
    BaseUserManager
)

from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password, **extra_fields):
        """
        Creates and saves a staff user with the given email and password.
        """

        user = self.create_user(
            email,
            password=password,
            **extra_fields,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        user = self.create_user(
            email,
            password=password,
            **extra_fields
        )

        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    Register_as = (
        ('Seller', 'Seller'),
        ('Buyer', 'Buyer'),
        ('Both', 'Both'),
    )
    email = models.EmailField(verbose_name='email', max_length=255, unique=True, blank=True, null=True, error_messages={
        'null': 'This feild cannot be nulll'
    })
    username = models.CharField(max_length=255, blank=True, null=True, unique=True)
    phone_number = models.CharField(max_length=13, blank=True, null=True, unique=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=10, choices=Register_as)
    room = models.ManyToManyField(to="accounts.Room", blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# This is Correct Method
class Room(models.Model):
    room = models.IntegerField(editable=False)


class Chat(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    text = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name="UserAllMessage",
                             default=None, blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE,
                             related_name="Room_Messages",
                             default=None, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    Updated_at = models.DateTimeField(default=timezone.now)


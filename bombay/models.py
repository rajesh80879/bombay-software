from datetime import datetime
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.db import models
from .managers import CustomUserManager

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    GENDER = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Others", "Others")

    )
    TYPE = (
        ("Primary", "Primary"),
        ("Secondary", "Secondary"),

    )
    firstname = models.CharField(max_length=80, default=None,null=True)
    lastname = models.CharField(max_length=80, default=None,null=True)
    dob = models.DateField(default=datetime.now())
    gender = models.CharField(choices=GENDER, max_length=10, default=None)
    email = models.EmailField(unique=True)
    contact = models.BigIntegerField(default=0, unique=True)
    type = models.CharField(choices=TYPE,max_length=10, default=None)
    password = models.CharField(max_length=255, default=None)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __str__(self):
        return self.email



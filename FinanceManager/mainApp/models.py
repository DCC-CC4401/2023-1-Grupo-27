from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    saldo = models.IntegerField(default=0)
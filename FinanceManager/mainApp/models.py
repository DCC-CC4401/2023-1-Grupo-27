from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    saldo = models.IntegerField(default=0)
    #apodo = models.CharField(max_length=30)
    #pronombres = [('La','La'),('El','El'), ('Le','Le'),('Otro','Otro')]
    #pronombre = models.CharField(max_length=5,choices=pronombres)
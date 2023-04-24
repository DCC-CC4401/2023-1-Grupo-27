from django.contrib import admin
from mainApp.models import User
from mainApp.models import Transaccion
from mainApp.models import RealizaTransaccion

# Register your models here.
admin.site.register(User)
admin.site.register(Transaccion)
admin.site.register(RealizaTransaccion)
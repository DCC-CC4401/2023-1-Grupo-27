from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    saldo = models.IntegerField(default=0)

class Transaccion(models.Model):  # Django añade un id por defecto
    nombre = models.CharField(max_length=250)  # un varchar
    tipos = [('Ingreso','Ingreso'),('Egreso','Egreso')] 
    tipo = models.CharField(max_length=8,choices=tipos) # Tipo = ingreso/egreso
    categoria = models.CharField(max_length=250, default=None, null=True) # Categoria que es null por defecto
    monto = models.IntegerField() # Un monto requerido de asignar

    def __str__(self): # Como se mostrara al imprimir
        return f'{self.nombre} ({self.categoria}): {self.monto}'
    
class RealizaTransaccion(models.Model):

    idUsuario = models.ForeignKey(User, on_delete=models.CASCADE) # Llave foranea a usuario
    idTransaccion = models.ForeignKey(Transaccion, on_delete=models.CASCADE) # Llave foranea a transaccion
    fecha = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))  # Un date de cuando se crea una transaccion
    
    def __str__(self): # Como se mostrara al imprimir
        return f'idUsuario: {self.idUsuario}, idTransaccion: {self.idTransaccion}, Fecha: {self.fecha}'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['idUsuario', 'idTransaccion'], name='unique_realizatransaccion')
        ]
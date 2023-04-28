from pyexpat.errors import messages
from django.db import IntegrityError
from django.db import models
from mainApp.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from .models import Transaccion
from django.urls import reverse
from django.shortcuts import render, get_object_or_404

def index(request):
    if request.method == "GET":
        user = request.user # Obtenemos el usuario
        transacciones = Transaccion.objects.filter(usuario=user.id) # Obtener transacciones del usuario
        saldo = saldo_usuario(request, user.id) # Obtener saldo del usuario
        return render(request, "index.html", {"transacciones": transacciones, "user": user, "saldo": saldo})
    if request.method == "POST":
        if "ingreso" in request.POST or "egreso" in request.POST:
            tipo = "Ingreso" if "ingreso" in request.POST else "Egreso"
            titulo = request.POST["titulo"]  # titulo de la transaccion
            nombre_categoria = request.POST["categoria"]  # Nombre de la categoria, en caso de que no se especifique sera el string vacio por defecto
            monto = request.POST["monto"]  # Monto del ingreso
            fecha = request.POST["fecha"] # Fecha de la transaccion
            if request.user.is_authenticated: # Creamos la transaccion con los datos obtenidos si el usuario esta autenticado
                if fecha != "": # Caso de que no se ingrese una fecha
                    nueva_transaccion = Transaccion(nombre=titulo, tipo=tipo, categoria=nombre_categoria, monto=monto, fecha=fecha, usuario=request.user) 
                else:
                    nueva_transaccion = Transaccion(nombre=titulo, tipo=tipo, categoria=nombre_categoria, monto=monto, usuario=request.user) 
                nueva_transaccion.save()  # Se guarda la transaccion en base de datos
        if "modificar" in request.POST:
            transaccion_id = request.POST.get('transaccion_id')
            transaccion = Transaccion.objects.get(id = transaccion_id)
            if request.user == transaccion.usuario:
                if request.POST["titulo"] != "":
                    transaccion.nombre = request.POST["titulo"]
                if request.POST["categoria"] != "":
                    transaccion.categoria = request.POST["categoria"]
                if request.POST["monto"] != "":
                    transaccion.monto = request.POST["monto"]
                if request.POST["fecha"] != "":
                    transaccion.fecha = request.POST["fecha"]
                if request.POST["tipo"] != 'opcion1':
                    if request.POST["tipo"] == 'opcion2':
                        transaccion.tipo = 'Ingreso'
                    if request.POST["tipo"] == 'opcion3':
                        transaccion.tipo = 'Egreso'
                transaccion.save()
    return redirect("/mainApp")

def register_user(request):
    if request.method == 'GET': #Si estamos cargando la página
        return render(request, "./register_user.html") #Mostrar el template

    elif request.method == 'POST': #Si estamos recibiendo el form de registro
        #Tomar los elementos del formulario que vienen en request.POST
        nombre = request.POST['nombre']
        contraseña = request.POST['contraseña']
        #apodo = request.POST['apodo']
        #pronombre = request.POST['pronombre']
        #mail = request.POST['mail']

        #Crear el nuevo usuario
        #user = User.objects.create_user(username=nombre, password=contraseña, email=mail, apodo=apodo, pronombre=pronombre)
        try:
            user = User.objects.create_user(username=nombre, password=contraseña)
            login(request,user)
            #Redireccionar la página /index
            return HttpResponseRedirect('/mainApp')
        except IntegrityError: # Caso en que el usuario con tal nombre ya exista
            return HttpResponseRedirect('.')



def login_user(request):
    if request.method == 'GET':
        return render(request,"./login.html")
    if request.method == 'POST':
        username = request.POST['username'] # Obtenemos nombre de usuario
        contraseña = request.POST['contraseña'] # Obtenemos su contraseña
        usuario = authenticate(username=username,password=contraseña) # Autenticamos el usuario
        if usuario is not None: # Si la respuesta de la autenticacion no fue None, el usuario existe y puede entrar
            login(request,usuario)
            return HttpResponseRedirect('../mainApp')
        else: # Caso contrario debe registrarse
            return HttpResponseRedirect('/login')
        
def logout_user(request):
    logout(request)
    return redirect("/mainApp")

def saldo_usuario(request, id_usuario):
    usuario = get_object_or_404(User, id=id_usuario)
    ingresos = Transaccion.objects.filter(usuario=usuario, tipo='Ingreso').aggregate(models.Sum('monto'))['monto__sum'] or 0
    egresos = Transaccion.objects.filter(usuario=usuario, tipo='Egreso').aggregate(models.Sum('monto'))['monto__sum'] or 0
    saldo = usuario.saldo + ingresos - egresos
    return str(saldo)
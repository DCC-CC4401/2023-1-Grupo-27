from pyexpat.errors import messages
from django.db import IntegrityError
from mainApp.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from .models import Transaccion

def index(request):
    if request.method == "GET":
        user = request.user # Obtenemos el usuario
        transacciones = Transaccion.objects.filter(usuario=user.id) # Obtener transacciones del usuario
        return render(request, "index.html", {"transacciones": transacciones, "user": user})
    
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
            return render(request, 'index.html')
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
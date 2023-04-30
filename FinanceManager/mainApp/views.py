from pyexpat.errors import messages
from django.db import IntegrityError
from django.db import models
from mainApp.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import Transaccion
from django.shortcuts import render, get_object_or_404

def index(request):  # Metodo para la pagina principal
    if request.method == "GET": # Se esta cargando la pagina
        user = request.user # Obtenemos el usuario
        transacciones = Transaccion.objects.filter(usuario=user.id) # Obtener transacciones del usuario
        saldo = saldo_usuario(user.id) # Obtener saldo del usuario
        return render(request, "index.html", {"transacciones": transacciones, "user": user, "saldo": saldo}) # Cargamos la pagina con lo correspondiente
    if request.method == "POST": # Se envía un formulario desde la pagina
        if "ingreso" in request.POST or "egreso" in request.POST: # Estamos recibiendo un post del modal de ingreso o egreso
            tipo = "Ingreso" if "ingreso" in request.POST else "Egreso" # Diferenciamos caso entre ingreso o egreso
            titulo = request.POST["titulo"]  # titulo de la transaccion
            nombre_categoria = request.POST["categoria"]  # Nombre de la categoria, en caso de que no se especifique sera el string vacio por defecto
            monto = request.POST["monto"]  # Monto del ingreso
            fecha = request.POST["fecha"] # Fecha de la transaccion
            if request.user.is_authenticated: # Creamos la transaccion con los datos obtenidos si el usuario esta autenticado
                if fecha != "": # Caso de que se ingrese una fecha
                    nueva_transaccion = Transaccion(nombre=titulo, tipo=tipo, categoria=nombre_categoria, monto=monto, fecha=fecha, usuario=request.user) 
                else: # Caso en que no se haya ingresado una fecha
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
        if "eliminar" in request.POST:
            transaccion_id = request.POST.get('transaccion_id')
            transaccion = Transaccion.objects.get(id = transaccion_id)
            if request.user == transaccion.usuario:
                transaccion.delete()
    return redirect("/mainApp")

def register_user(request): # Metodo para registrar al usuario
    if request.method == 'GET': #Si estamos cargando la página
        return render(request, "./register_user.html") #Mostrar el template

    elif request.method == 'POST': #Si estamos recibiendo el form de registro
        #Tomar los elementos del formulario que vienen en request.POST
        nombre = request.POST['nombre'] # Guardamos el nombre de usuario
        contraseña = request.POST['contraseña'] # Guardamos la contraseña del usuario

        try: # Intentamos crear un nuevo usuario
            user = User.objects.create_user(username=nombre, password=contraseña) #Creamos un nuevo usuario con los datos recien obtenidos 
            login(request,user) # Logeamos al usuario recien creado
            #Redireccionar la página /index
            return HttpResponseRedirect('/mainApp')
        except IntegrityError: # Caso en que el usuario con tal nombre ya exista, recargamos la pagina
            return HttpResponseRedirect('.')



def login_user(request): # Metodo para hacer login a un usuario
    if request.method == 'GET': # Si estamos cargando la pagina
        return render(request,"./login.html") # Cargamos el html
    if request.method == 'POST': # Cuando se envía algo de la pagina (form)
        username = request.POST['username'] # Obtenemos nombre de usuario
        contraseña = request.POST['contraseña'] # Obtenemos su contraseña
        usuario = authenticate(username=username,password=contraseña) # Autenticamos el usuario
        if usuario is not None: # Si la respuesta de la autenticacion no fue None, el usuario existe y puede entrar
            login(request,usuario) # Se logea el usuario
            return HttpResponseRedirect('../mainApp') # Ingresamos a la pagina principal
        else: # Caso contrario debe registrarse, o bien se equivoco al ingresar datos
            return HttpResponseRedirect('/login') # Recargamos la pagina
        
def logout_user(request): # Metodo para hacer logout de un user
    logout(request) # Hacemos logout del usuario
    return redirect("/mainApp") # Redireccionamos a la pagina de inicio

def saldo_usuario(id_usuario):
    if id_usuario is not None:
        usuario = get_object_or_404(User, id=id_usuario)
        ingresos = Transaccion.objects.filter(usuario=usuario, tipo='Ingreso').aggregate(models.Sum('monto'))['monto__sum'] or 0
        egresos = Transaccion.objects.filter(usuario=usuario, tipo='Egreso').aggregate(models.Sum('monto'))['monto__sum'] or 0
        saldo = usuario.saldo + ingresos - egresos
    else:
        saldo = 0
    return str(saldo)
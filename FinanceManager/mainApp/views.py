from pyexpat.errors import messages
from django.db import IntegrityError
from django.db import models
from mainApp.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import Transaccion
from django.shortcuts import render, get_object_or_404
from django.template.defaulttags import register
from django.contrib.humanize.templatetags.humanize import intcomma
import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

def index(request):  # Metodo para la pagina principal
    if request.method == "GET": # Se esta cargando la pagina
        user = request.user # Obtenemos el usuario
        transacciones = Transaccion.objects.filter(usuario=user.id).order_by('-fecha') # Obtener transacciones del usuario ordenadas por fecha descendiente
        saldo = saldo_usuario(user.id) # Obtener saldo del usuario
        categorias_form = agregar_categorias_form() # Para crear las categorias iterativamente al momento de cargar la pagina
        
        # Obtenemos la fecha de inicio almacenada en la sesión
        fecha_inicio = request.session.get("fecha_inicio", "1900-01-01")
        fecha_termino = request.session.get("fecha_termino", "9999-12-31")

        # Actualizamos la fecha de inicio en la sesión si se proporciona en la solicitud GET
        if "fecha_inicio" in request.GET:
            if request.GET.get("fecha_inicio") == "":   #Si se borra la fecha, se vuelve a la por defecto
                fecha_inicio = "1900-01-01"
            else:
                fecha_inicio = request.GET["fecha_inicio"]  #obtenemos la fecha ingresada
            request.session["fecha_inicio"] = fecha_inicio  #Guardamos la fecha ingresada en la sesion
        if "fecha_termino" in request.GET:
            if request.GET.get("fecha_termino") == "":  #Si se borra la fecha, se vuelve a la por defecto
                fecha_termino = "9999-12-31"
            else:
                fecha_termino=request.GET["fecha_termino"]  #obtenemos la fecha ingresada
            request.session["fecha_termino"] = fecha_termino    #Guardamos la fecha ingresada en la sesion
        
        #Obtenemos el filtro guardado en la sesion
        filtercat = request.session.get("categoriaEscoger", "")
        
        # Actualizamos el filtro de categoria en la sesión si se proporciona en la solicitud GET
        if "categoriaEscoger" in request.GET:
            if request.GET.get("categoriaEscoger") == "":   #Si se elimina el filtro, se vuelve a un valor por defecto
                filtercat = ""
            else:
                filtercat = request.GET["categoriaEscoger"]  #obtenemos el filtro ingresado
            request.session["categoriaEscoger"] = filtercat  #Guardamos el filtro en la sesion

        return render(request, "index.html", {"transacciones": transacciones, "user": user, "saldo": saldo, "categorias_form": categorias_form, "fecha_inicio":fecha_inicio, "fecha_termino":fecha_termino, "filtercat":filtercat}) # Cargamos la pagina con lo correspondiente
    
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
        if "modificar" in request.POST:#Recibimos un post del modal de modificacion de transaccion
            transaccion_id = request.POST.get('transaccion_id')# obtenemos el id de la transaccion
            transaccion = Transaccion.objects.get(id = transaccion_id) #obtenemos la transaccion a partir de el id encontrado
            if request.user == transaccion.usuario: #Se confirma que el usuario actual sea el dueño de la transaccion que se quiere modificar
                if request.POST["titulo"] != "": #Confirmamos que se haya escrito algo en la casilla de nuevo titulo
                    transaccion.nombre = request.POST["titulo"] #Reemplazamos el titulo actual por el nuevo titulo ingresado
                if request.POST["categoria"] != "sinCambios": #Confirmamos que se haya escrito algo en la casilla de nueva categoria
                    transaccion.categoria = request.POST["categoria"] #Reemplazamos la categoria actual por la nueva categoria ingresada
                if request.POST["monto"] != "": #Confirmamos que se haya escrito algo en la casilla de nuevo monto
                    transaccion.monto = request.POST["monto"] #Reemplazamos el monto actual por el nuevo monto ingresado
                if request.POST["fecha"] != "": #Confirmamos que se haya escrito algo en la casilla de nueva fecha
                    transaccion.fecha = request.POST["fecha"] #Reemplazamos la fecha actual por la nueva fecha ingresada
                if request.POST["tipo"] != 'opcion1': #verificamos el nuevo tipo de transaccion que quiere asignar
                    if request.POST["tipo"] == 'opcion2': #Se cambia el tipo de la transaccion actual a Ingreso
                        transaccion.tipo = 'Ingreso'
                    if request.POST["tipo"] == 'opcion3': #Se cambia el tipo de la transaccion actual a Egreso
                        transaccion.tipo = 'Egreso'
                transaccion.save() #Se guarda la transaccion con los nuevos datos
        if "eliminar" in request.POST: #Recibimos un post del modal de modificacion de transaccion
            transaccion_id = request.POST.get('transaccion_id') #obtenemos el id de la transaccion
            transaccion = Transaccion.objects.get(id = transaccion_id) #obtenemos la transaccion a partir de el id encontrado
            if request.user == transaccion.usuario: #Se confirma que el usuario actual sea el dueño de la transaccion que se quiere modificar
                transaccion.delete() #Se elimina la transaccion actual
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
            return render(request, 'register_user.html', {'errorRegistro': True})


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
            return render(request, './login.html', {'errorInicio': True})
        
def logout_user(request): # Metodo para hacer logout de un user
    logout(request) # Hacemos logout del usuario
    return redirect("/mainApp") # Redireccionamos a la pagina de inicio

def saldo_usuario(id_usuario): # Metodo para conseguir el saldo de un usuario
    if id_usuario is not None: # Si el usuario no es nulo
        usuario = get_object_or_404(User, id=id_usuario) # Obtenemos el usuario
        ingresos = Transaccion.objects.filter(usuario=usuario, tipo='Ingreso').aggregate(models.Sum('monto'))['monto__sum'] or 0 # Obtenemos la suma de todos sus ingresos
        egresos = Transaccion.objects.filter(usuario=usuario, tipo='Egreso').aggregate(models.Sum('monto'))['monto__sum'] or 0 # Obtenemos la suma de todos sus egresos
        saldo = usuario.saldo + ingresos - egresos # Calculamos el saldo del usuario
    else: # Caso usuario nulo, saldo es por defecto 0
        saldo = 0
    return saldo # Devolvemos el saldo del usuario

# Filtro para agregar separador de miles
@register.filter
def intdot(value):
    return intcomma(value).replace(",", ".") # Usamos el filtro intcomma, pero cambiamos las comas por puntos para el formato latinoamericano

# Categorias para transacciones
def agregar_categorias_form():
    CATEGORIAS = (
        "Transporte",
        "Ejercicio",
        "Familia",
        "Supermercado",
        "Regalos",
        "Educacion",
        "Salidas",
        "Hogar",
        "Salud",
        "Otro"
    )
    return CATEGORIAS

@login_required
def exportar_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transacciones.csv"'
    writer = csv.writer(response) # Se crea el escritor de CSV
    usuario = request.user  # Obtener el usuario logeado
    datos = Transaccion.objects.filter(usuario=usuario)  # Filtrar los datos por usuario

    # Obtener los nombres de las columnas
    columnas = [field.name for field in Transaccion._meta.get_fields() if field.concrete]

    # Eliminamos la columna 'usuario'
    columna_eliminar = 'usuario'
    if columna_eliminar in columnas:
        columnas.remove(columna_eliminar)

    writer.writerow(columnas)  # Escribimos los encabezados de las columnas
    for dato in datos:
        fila = model_to_dict(dato, fields=list(columnas))  # Convertir el objeto en un diccionario
        writer.writerow(fila.values())  # Escribir los valores en el archivo CSV
    return response
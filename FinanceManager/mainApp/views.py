from mainApp.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader


def index(request):
    template = loader.get_template('./index.html')
    return HttpResponse(template.render())

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
        user = User.objects.create_user(username=nombre, password=contraseña)


        #Redireccionar la página /index
        return HttpResponseRedirect('/index')
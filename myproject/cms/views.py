from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

from .models import Persona

FORMULARIO = """
<form action="" method="POST">
  Nombre: <input type="text" name="nombre"><br>
  Descripcion: <input type="text" name="descripcion"><br>
  <input type="submit" value="Enviar">
</form>
"""

def barra(request):
    if request.user.is_authenticated():
        logged = 'Logged in as ' + request.user.username + '. <a href="/logout">Logout</a>'
    else:
        logged = 'Not logged in. <a href="/login">Login</a>'
    personas = Persona.objects.all()
    respuesta = "<ul>"
    for persona in personas:
        respuesta += '<li>' + "  " + str(persona.id) + "--->" + persona.nombre + ":  con la siguiente descripcion:   " + persona.descripcion
    respuesta += "</ul>"
    return HttpResponse(logged + "<br>" + respuesta)


@csrf_exempt
def persona(request, num):
    if request.method == "POST":
        persona = Persona(nombre = request.POST['nombre'], descripcion = request.POST['descripcion'])
        persona.save()
        HttpResponse("La nueva persona es: " + persona.nombre + " con descripcion: " + persona.descripcion)
    try:
        persona = Persona.objects.get(id=int(num))
    except Persona.DoesNotExist:
        return HttpResponse("Esa persona no existe")
    respuesta = "Id: " + str(persona.id) + "<br>"
    respuesta += "Nombre: " + persona.nombre + "<br>"
    respuesta += "Descripcion: " + persona.descripcion
    if request.user.is_authenticated():
        respuesta += "<br><br>" + FORMULARIO
    else:
        respuesta += "<br><br>" + "Se necesita login para introducir persona nueva: <a href='/login/'>Login</a>"
    return HttpResponse(respuesta)

#edit permite editar solo personas guardas en la base de datos. No puede editar personas que no esten en la BD
@csrf_exempt
def edit(request, num):
    if request.method == "POST":
        persona = Persona.objects.get(id=int(num))
        nueva_persona = Persona(id=persona.id, nombre = request.POST["nombre"], descripcion = request.POST["descripcion"]) 
        nueva_persona.save(force_update=True)
        HttpResponse("La nueva persona es: " + nueva_persona.nombre + " con descripcion: " + nueva_persona.descripcion)
    try:
        persona = Persona.objects.get(id=int(num))
    except Persona.DoesNotExist:
        return HttpResponse("La persona " + num +  " no está guardada")
    if request.user.is_authenticated():
        respuesta = 'Logged in as ' + request.user.username + '. <a href="/logout">Logout</a>' + "<br><br>" + FORMULARIO
    else:
        respuesta = 'Not logged in. Necesitas estar autenticado para editar personas <a href="/login">Login</a>'
    return HttpResponse(respuesta)
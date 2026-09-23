from django.shortcuts import render
from django.http import HttpResponse
import datetime

def trabajador(request):
    datos = {
        'nombre':'armando',
        'apellidos':'bronca segura',
        'cargo':'bodeguero'
    }
    return render(request,'bodega/inicio.html',datos)



# Create your views here.
def productos(request):
    return HttpResponse("<h1>productos desde bodega </h1>")

def ahora(request):
    fecha = datetime.datetime.now()
    salida = f"<h2>en la bodega hoy es <b>{fecha}</b></h2>"
    return HttpResponse(salida)
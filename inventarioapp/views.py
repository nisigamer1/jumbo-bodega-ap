from django.shortcuts import render
from django.http import HttpResponse
import datetime

# Create your views here.
def inventario(request):
    return render(request,'inventario/inicio.html')

def inicio(request):
#variable que muestra la url de inicio de la pagina y su contenico  que contiene una variable salida que tiene lenguaje html

    salida =''' 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>mi terrible de dejango</title>
</head>
<body>
<h1>bienvenidos a mi terrible sitio</h1>   
</body>
</html>'''
    return HttpResponse(salida)

def ahora(request):
    fecha = datetime.datetime.now()
    salida = f"<h2>en la tienda  hoy es <b>{fecha}</b></h2>"
    return HttpResponse(salida)
def home(request):
    return HttpResponse("<h1>pagina inicial del proyecto</h1>")
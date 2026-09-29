from django.shortcuts import render
from datetime import datetime
from .models import Producto

def inicio(request):
    return render(request, 'inventario/main.html')

def inventario(request):
    query = request.GET.get('q', '')
    if query:
        productos = Producto.objects.filter(nombre__icontains=query) | Producto.objects.filter(codigo_barras__icontains=query)
    else:
        productos = Producto.objects.all()
    return render(request, 'inventario/main.html', {'productos': productos, 'query': query})

def ahora(request):
    return render(request, 'inventario/ahora.html', {'fecha_actual': datetime.now()})
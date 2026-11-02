from django.shortcuts import render
from datetime import datetime
from django.db.models import Q, Sum
from django.contrib.auth.models import User  # <-- Importación agregada
from .models import Empleado, Producto

def inicio(request):
    return render(request, 'bodega/inicio.html')

def empleados(request):
    trabajadores = User.objects.select_related('perfilempleado').all()
    return render(request, 'bodega/empleados.html', {'trabajadores': trabajadores})

def productos(request):
    query = request.GET.get('q', '').strip()
    if query:
        productos_list = Producto.objects.filter(
            Q(nombre__icontains=query) | 
            Q(codigo_barras__icontains=query) |
            Q(categoria__nombre__icontains=query)
        ).select_related('categoria')
    else:
        productos_list = Producto.objects.all().select_related('categoria')

    total_sala = productos_list.aggregate(total=Sum('stock_sala'))['total'] or 0
    total_bodega = productos_list.aggregate(total=Sum('stock_bodega'))['total'] or 0
    total_items = productos_list.count()
        
    return render(request, 'bodega/productos.html', {
        'productos': productos_list,
        'query': query,
        'total_sala': total_sala,
        'total_bodega': total_bodega,
        'total_items': total_items,
    })

def ahora(request):
    return render(request, 'bodega/ahora.html', {'fecha_actual': datetime.now()})
from django.shortcuts import render
from datetime import datetime
from django.db.models import Q, Sum
from .models import Empleado, Producto

def inicio(request):
    # Consulta los trabajadores activos para mostrarlos en la página de inicio
    trabajadores = Empleado.objects.filter(activo=True).select_related('departamento')
    return render(request, 'bodega/inicio.html', {'trabajadores': trabajadores})

def empleados(request):
    query = request.GET.get('q', '').strip()
    if query:
        empleados_list = Empleado.objects.filter(
            Q(nombres__icontains=query) | 
            Q(apellidos__icontains=query) | 
            Q(rut__icontains=query) |
            Q(cargo__icontains=query) |
            Q(departamento__nombre__icontains=query)
        ).select_related('departamento')
    else:
        empleados_list = Empleado.objects.all().select_related('departamento')
        
    return render(request, 'bodega/empleados.html', {
        'empleados': empleados_list, 
        'query': query
    })

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

    # Totales para los contadores superiores
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
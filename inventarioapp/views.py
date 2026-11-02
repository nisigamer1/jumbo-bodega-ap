from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from .models import Producto, Categoria
from django.contrib.auth.decorators import login_required

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

@login_required
def catalogo_productos(request):
    productos = Producto.objects.all()
    return render(request, 'inventario/catalogo.html', {'productos': productos})

# Vistas del Mantenedor (CRUD)
@login_required
def mantenedor_productos(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo_barras')
        nombre = request.POST.get('nombre')
        cat_id = request.POST.get('categoria')
        precio = request.POST.get('precio')
        stock_sala = request.POST.get('stock_sala')
        stock_bodega = request.POST.get('stock_bodega')
        
        categoria = get_object_or_404(Categoria, id=cat_id)
        
        Producto.objects.create(
            codigo_barras=codigo,
            nombre=nombre,
            categoria=categoria,
            precio=precio,
            stock_sala=stock_sala,
            stock_bodega=stock_bodega
        )
        return redirect('mantenedor_productos')

    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'inventario/mantenedor_productos.html', {
        'productos': productos,
        'categorias': categorias
    })

@login_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    return redirect('mantenedor_productos')
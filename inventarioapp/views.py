from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.contrib import messages # Importante para los SweetAlerts
from django.contrib.auth.decorators import login_required

from .models import Producto, Categoria
from .forms import ProductoForm # Importamos el formulario nativo

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

# ==========================================
# VISTAS DEL MANTENEDOR DE PRODUCTOS (CRUD)
# ==========================================

@login_required
def mantenedor_productos(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto agregado exitosamente.')
            return redirect('mantenedor_productos')
        else:
            messages.error(request, 'Error al guardar el producto. Revisa los datos.')
    else:
        form = ProductoForm()

    productos = Producto.objects.select_related('categoria').all()
    
    return render(request, 'inventario/mantenedor_productos.html', {
        'productos': productos,
        'form': form
    })

@login_required
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    
    if request.method == 'POST':
        # Le pasamos el instance para que sobreescriba el existente
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado correctamente.')
            return redirect('mantenedor_productos')
        else:
            messages.error(request, 'Error al actualizar. Revisa los datos.')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'inventario/editar_producto.html', {
        'form': form, 
        'producto': producto
    })

@login_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    nombre_prod = producto.nombre # Guardamos el nombre antes de borrar
    producto.delete()
    messages.success(request, f'Producto "{nombre_prod}" eliminado del sistema.')
    return redirect('mantenedor_productos')
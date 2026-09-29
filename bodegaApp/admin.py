from django.contrib import admin
from .models import Departamento, Empleado, Categoria, Producto

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'codigo_area')
    search_fields = ('nombre', 'codigo_area')

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombres', 'apellidos', 'cargo', 'departamento', 'turno', 'activo')
    list_filter = ('activo', 'departamento', 'turno')
    search_fields = ('rut', 'nombres', 'apellidos', 'cargo')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pasillo')
    search_fields = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    # Agregamos 'stock_total' al final de list_display
    list_display = ('codigo_barras', 'nombre', 'categoria', 'precio', 'stock_bodega', 'stock_sala', 'stock_total', 'en_oferta')
    list_filter = ('categoria', 'en_oferta')
    search_fields = ('codigo_barras', 'nombre')
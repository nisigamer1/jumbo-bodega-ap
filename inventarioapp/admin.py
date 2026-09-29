from django.contrib import admin
from .models import Categoria, Producto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'pasillo')
    search_fields = ('nombre',)
    ordering = ('pasillo',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo_barras', 'nombre', 'categoria', 'precio', 'stock_bodega', 'stock_sala', 'stock_total', 'en_oferta')
    list_filter = ('categoria', 'en_oferta')
    search_fields = ('codigo_barras', 'nombre')
    list_editable = ('precio', 'stock_bodega', 'stock_sala', 'en_oferta')

    def stock_total(self, obj):
        return obj.stock_total()
    stock_total.short_description = "Stock Total"
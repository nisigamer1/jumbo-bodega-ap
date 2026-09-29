from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Categoría de Producto")
    pasillo = models.IntegerField(verbose_name="Pasillo de Exhibición en Sala", default=1)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías de Productos"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} (Pasillo {self.pasillo})"


class Producto(models.Model):
    codigo_barras = models.CharField(max_length=20, unique=True, verbose_name="Código EAN / SKU")
    nombre = models.CharField(max_length=150, verbose_name="Nombre del Producto")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="productos", verbose_name="Categoría")
    precio = models.IntegerField(verbose_name="Precio Venta Jumbo ($)")
    stock_bodega = models.IntegerField(default=0, verbose_name="Stock en Bodega AP")
    stock_sala = models.IntegerField(default=0, verbose_name="Stock en Sala de Ventas")
    fecha_vencimiento = models.DateField(blank=True, null=True, verbose_name="Fecha Próxima de Vencimiento")
    en_oferta = models.BooleanField(default=False, verbose_name="¿Producto en Oferta Jumbo?")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos e Inventario"
        ordering = ['nombre']

    def stock_total(self):
        return self.stock_bodega + self.stock_sala

    def __str__(self):
        return f"{self.nombre} - Stock Total: {self.stock_total()} un."
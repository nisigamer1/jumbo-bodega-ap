from django.db import models

# ==========================================
# 1. MÓDULO TRABAJADORES
# ==========================================
class Departamento(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Área/Departamento")
    codigo_area = models.CharField(max_length=10, unique=True, verbose_name="Código Áreas Jumbo (Ej: BOD-AP, SALA-01)")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción de Responsabilidades")

    class Meta:
        verbose_name = "Departamento / Área"
        verbose_name_plural = "Departamentos y Áreas"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.codigo_area})"


class Empleado(models.Model):
    TURNOS = [
        ('MAÑANA', 'Turno Mañana (07:00 - 15:00)'),
        ('TARDE', 'Turno Tarde (14:30 - 22:00)'),
        ('NOCHE', 'Turno Noche / Reposición (21:30 - 07:00)'),
    ]

    rut = models.CharField(max_length=12, unique=True, verbose_name="RUT Trabajador")
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    cargo = models.CharField(max_length=100, verbose_name="Cargo (Ej: Bodeguero AP, Reponedor Sala, Supervisor)")
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="empleados", verbose_name="Área de Trabajo")
    turno = models.CharField(max_length=20, choices=TURNOS, default='MAÑANA', verbose_name="Turno Asignado")
    fecha_ingreso = models.DateField(verbose_name="Fecha de Ingreso")
    activo = models.BooleanField(default=True, verbose_name="¿Trabajador Activo en Jumbo?")

    class Meta:
        verbose_name = "Trabajador Jumbo"
        verbose_name_plural = "Trabajadores Jumbo"
        ordering = ['apellidos', 'nombres']

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

    def __str__(self):
        return f"{self.rut} - {self.nombre_completo} [{self.cargo}]"

# ==========================================
# 2. MÓDULO INVENTARIO Y PRODUCTOS
# ==========================================
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

    @property  # <--- Agregado para tratarse como atributo
    def stock_total(self):
        return (self.stock_bodega or 0) + (self.stock_sala or 0)

    def __str__(self):
        return f"{self.nombre} - Stock Total: {self.stock_total} un."
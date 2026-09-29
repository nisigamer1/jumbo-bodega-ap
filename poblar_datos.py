import os
import django
from datetime import date

# Configuramos el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from bodegaApp.models import Categoria, Producto, Departamento, Empleado

print("Iniciando la carga de datos para Jumbo Bodega AP...")

# Detectamos los campos reales de tu modelo Empleado
campos_empleado = [f.name for f in Empleado._meta.fields]
print(f"Campos reales detectados en tu modelo Empleado: {campos_empleado}\n")

# 1. Departamentos
deptos_data = [
    {"nombre": "Bodega AP", "codigo_area": "DEP-01"},
    {"nombre": "Recepción y Logística", "codigo_area": "DEP-02"},
    {"nombre": "Reposición Sala", "codigo_area": "DEP-03"},
    {"nombre": "Control de Inventario", "codigo_area": "DEP-04"},
    {"nombre": "Cocina y Comidas Preparadas", "codigo_area": "DEP-05"},
]

deptos = {}
for d in deptos_data:
    obj, _ = Departamento.objects.get_or_create(
        nombre=d["nombre"],
        defaults={"codigo_area": d["codigo_area"]}
    )
    deptos[d["nombre"]] = obj

print("✓ Departamentos creados.")

# 2. Empleados (Tus compañeros y tú)
empleados_raw = [
    {"rut": "19.876.543-2", "nombre": "Nicolás", "apellido": "Véliz", "cargo": "Operador Grúa Horquilla / Bodeguero", "depto": deptos["Bodega AP"], "email": "nicolas.veliz@jumbo.cl", "telefono": "+56912345678"},
    {"rut": "19.123.456-1", "nombre": "Nicolás", "apellido": "Alegre", "cargo": "Bodeguero", "depto": deptos["Bodega AP"], "email": "nicolas.alegre@jumbo.cl", "telefono": "+56911112222"},
    {"rut": "20.234.567-2", "nombre": "Marlyn", "apellido": "Katalyna", "cargo": "Reponedora", "depto": deptos["Reposición Sala"], "email": "marlyn.katalyna@jumbo.cl", "telefono": "+56922223333"},
    {"rut": "20.345.678-3", "nombre": "Tobías", "apellido": "Gaete", "cargo": "Reponedor", "depto": deptos["Reposición Sala"], "email": "tobias.gaete@jumbo.cl", "telefono": "+56933334444"},
    {"rut": "20.456.789-4", "nombre": "Brad", "apellido": "André", "cargo": "Reponedor", "depto": deptos["Reposición Sala"], "email": "brad.andre@jumbo.cl", "telefono": "+56944445555"},
    {"rut": "18.567.890-5", "nombre": "Nelson", "apellido": "Moraga", "cargo": "Recepcionista", "depto": deptos["Recepción y Logística"], "email": "nelson.moraga@jumbo.cl", "telefono": "+56955556666"},
    {"rut": "20.678.901-6", "nombre": "Benjamín", "apellido": "Araya", "cargo": "Reponedor", "depto": deptos["Reposición Sala"], "email": "benjamin.araya@jumbo.cl", "telefono": "+56966667777"},
    {"rut": "20.789.012-7", "nombre": "Antonia", "apellido": "Castillo", "cargo": "Cocinera", "depto": deptos["Cocina y Comidas Preparadas"], "email": "antonia.castillo@jumbo.cl", "telefono": "+56977778888"},
    {"rut": "20.890.123-8", "nombre": "Diego", "apellido": "Guy", "cargo": "Reponedor", "depto": deptos["Reposición Sala"], "email": "diego.guy@jumbo.cl", "telefono": "+56988889999"},
]

for emp in empleados_raw:
    defaults = {}
    
    # Manejo dinámico de Nombres
    if "nombre_completo" in campos_empleado:
        defaults["nombre_completo"] = f"{emp['nombre']} {emp['apellido']}"
    elif "nombre" in campos_empleado and "apellido" in campos_empleado:
        defaults["nombre"] = emp["nombre"]
        defaults["apellido"] = emp["apellido"]
    elif "nombre" in campos_empleado:
        defaults["nombre"] = f"{emp['nombre']} {emp['apellido']}"

    # Cargo y Departamento
    if "cargo" in campos_empleado:
        defaults["cargo"] = emp["cargo"]
    if "departamento" in campos_empleado:
        defaults["departamento"] = emp["depto"]

    # Fechas obligatorias
    if "fecha_ingreso" in campos_empleado:
        defaults["fecha_ingreso"] = date(2024, 1, 15)
    if "fecha_contratacion" in campos_empleado:
        defaults["fecha_contratacion"] = date(2024, 1, 15)

    # Email / Correo
    if "email" in campos_empleado:
        defaults["email"] = emp["email"]
    elif "correo" in campos_empleado:
        defaults["correo"] = emp["email"]

    # Teléfono
    if "telefono" in campos_empleado:
        defaults["telefono"] = emp["telefono"]
    elif "fono" in campos_empleado:
        defaults["fono"] = emp["telefono"]
    elif "celular" in campos_empleado:
        defaults["celular"] = emp["telefono"]

    # Creación / Actualización
    if "rut" in campos_empleado:
        Empleado.objects.get_or_create(rut=emp["rut"], defaults=defaults)
    else:
        Empleado.objects.create(**defaults)

print("✓ Empleados en turno cargados (Equipo completo).")

# 3. Categorías con Pasillos
categorias_data = [
    {"nombre": "Abarrotes", "pasillo": 1},
    {"nombre": "Lácteos y Quesos", "pasillo": 2},
    {"nombre": "Bebidas y Licores", "pasillo": 3},
    {"nombre": "Limpieza y Hogar", "pasillo": 4},
    {"nombre": "Panadería y Dulces", "pasillo": 5},
    {"nombre": "Carnes y Cecinas", "pasillo": 6},
    {"nombre": "Congelados", "pasillo": 7},
]

cats = {}
for c in categorias_data:
    obj, _ = Categoria.objects.get_or_create(
        nombre=c["nombre"],
        defaults={"pasillo": c["pasillo"]}
    )
    cats[c["nombre"]] = obj

print("✓ Categorías creadas.")

# 4. Productos Reales de Jumbo (25 Ítems)
productos_data = [
    # Abarrotes
    {"codigo_barras": "780123400001", "nombre": "Arroz Grado 1 Tucapel 1kg", "categoria": cats["Abarrotes"], "precio": 1490, "stock_bodega": 120, "stock_sala": 45},
    {"codigo_barras": "780123400002", "nombre": "Aceite Vegetal Belmont 1L", "categoria": cats["Abarrotes"], "precio": 2190, "stock_bodega": 90, "stock_sala": 30},
    {"codigo_barras": "780123400003", "nombre": "Fideos Tallarin Lucchetti 400g", "categoria": cats["Abarrotes"], "precio": 990, "stock_bodega": 200, "stock_sala": 80},
    {"codigo_barras": "780123400004", "nombre": "Nescafé Tradición 170g", "categoria": cats["Abarrotes"], "precio": 5490, "stock_bodega": 60, "stock_sala": 25},
    {"codigo_barras": "780123400005", "nombre": "Atún Lomo al Agua Robinson Crusoe 160g", "categoria": cats["Abarrotes"], "precio": 1390, "stock_bodega": 150, "stock_sala": 50},
    
    # Lácteos y Quesos
    {"codigo_barras": "780123400006", "nombre": "Leche Entera Soprole 1L", "categoria": cats["Lácteos y Quesos"], "precio": 1050, "stock_bodega": 300, "stock_sala": 100},
    {"codigo_barras": "780123400007", "nombre": "Queso Gauda Laminado Soprole 250g", "categoria": cats["Lácteos y Quesos"], "precio": 2890, "stock_bodega": 80, "stock_sala": 35},
    {"codigo_barras": "780123400008", "nombre": "Mantequilla con Sal Soprole 250g", "categoria": cats["Lácteos y Quesos"], "precio": 2690, "stock_bodega": 70, "stock_sala": 20},
    {"codigo_barras": "780123400009", "nombre": "Yogur Batido Colun Frutilla 120g", "categoria": cats["Lácteos y Quesos"], "precio": 390, "stock_bodega": 250, "stock_sala": 90},

    # Bebidas y Licores
    {"codigo_barras": "780123400010", "nombre": "Coca-Cola Sabor Original 1.5L", "categoria": cats["Bebidas y Licores"], "precio": 1790, "stock_bodega": 180, "stock_sala": 60},
    {"codigo_barras": "780123400011", "nombre": "Cerveza Heineken Pack 6 Latas 350ml", "categoria": cats["Bebidas y Licores"], "precio": 5990, "stock_bodega": 100, "stock_sala": 40},
    {"codigo_barras": "780123400012", "nombre": "Agua Mineral Cachantun Sin Gas 1.5L", "categoria": cats["Bebidas y Licores"], "precio": 890, "stock_bodega": 220, "stock_sala": 75},

    # Limpieza y Hogar
    {"codigo_barras": "780123400013", "nombre": "Detergente Líquido Omo Diluible 500ml", "categoria": cats["Limpieza y Hogar"], "precio": 6490, "stock_bodega": 50, "stock_sala": 20},
    {"codigo_barras": "780123400014", "nombre": "Papel Higiénico Elite Rinde Más 8 Rollos", "categoria": cats["Limpieza y Hogar"], "precio": 4290, "stock_bodega": 110, "stock_sala": 40},
    {"codigo_barras": "780123400015", "nombre": "Lavaloza Cif Limón 750ml", "categoria": cats["Limpieza y Hogar"], "precio": 1890, "stock_bodega": 90, "stock_sala": 30},

    # Panadería y Dulces
    {"codigo_barras": "780123400016", "nombre": "Pan de Molde Blanco Ideal Familiar", "categoria": cats["Panadería y Dulces"], "precio": 2390, "stock_bodega": 60, "stock_sala": 25},
    {"codigo_barras": "780123400017", "nombre": "Galletas Tritón Chocolate 126g", "categoria": cats["Panadería y Dulces"], "precio": 850, "stock_bodega": 160, "stock_sala": 60},
    {"codigo_barras": "780123400018", "nombre": "Chocolate Sahne Nuss 250g", "categoria": cats["Panadería y Dulces"], "precio": 3990, "stock_bodega": 85, "stock_sala": 30},
    {"codigo_barras": "780123400019", "nombre": "Papas Fritas Lay's Corte Liso 250g", "categoria": cats["Panadería y Dulces"], "precio": 2290, "stock_bodega": 120, "stock_sala": 45},

    # Carnes y Cecinas
    {"codigo_barras": "780123400020", "nombre": "Jamón Pechuga de Pavo San Jorge 200g", "categoria": cats["Carnes y Cecinas"], "precio": 2490, "stock_bodega": 75, "stock_sala": 30},
    {"codigo_barras": "780123400021", "nombre": "Lomo Vetado Vacuno 1kg", "categoria": cats["Carnes y Cecinas"], "precio": 12990, "stock_bodega": 30, "stock_sala": 12},

    # Congelados
    {"codigo_barras": "780123400022", "nombre": "Helado Savory Cassata Chocochips 1L", "categoria": cats["Congelados"], "precio": 3290, "stock_bodega": 45, "stock_sala": 18},
    {"codigo_barras": "780123400023", "nombre": "Papas Prefritas Minuto Verde 1kg", "categoria": cats["Congelados"], "precio": 3490, "stock_bodega": 60, "stock_sala": 25},
    {"codigo_barras": "780123400024", "nombre": "Hamburguesa Vacuno La Crianza 4 un.", "categoria": cats["Congelados"], "precio": 3890, "stock_bodega": 70, "stock_sala": 28},
    {"codigo_barras": "780123400025", "nombre": "Verduras Surtidas Minuto Verde 500g", "categoria": cats["Congelados"], "precio": 1590, "stock_bodega": 80, "stock_sala": 35},
]

for p in productos_data:
    Producto.objects.get_or_create(
        codigo_barras=p["codigo_barras"],
        defaults={
            "nombre": p["nombre"],
            "categoria": p["categoria"],
            "precio": p["precio"],
            "stock_bodega": p["stock_bodega"],
            "stock_sala": p["stock_sala"]
        }
    )

print("✓ 25 Productos cargados correctamente.")
print("\n¡Base de datos poblada exitosamente con todo tu equipo!")
import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from bodegaApp.models import Empleado

# Datos reales del equipo Jumbo AP
equipo = [
    {"rut": "19.876.543-2", "nombres": "Nicolás", "apellidos": "Véliz"},
    {"rut": "19.123.456-1", "nombres": "Nicolás", "apellidos": "Alegre"},
    {"rut": "20.234.567-2", "nombres": "Marlyn", "apellidos": "Katalyna"},
    {"rut": "20.345.678-3", "nombres": "Tobías", "apellidos": "Gaete"},
    {"rut": "20.456.789-4", "nombres": "Brad", "apellidos": "André"},
    {"rut": "18.567.890-5", "nombres": "Nelson", "apellidos": "Moraga"},
    {"rut": "20.678.901-6", "nombres": "Benjamín", "apellidos": "Araya"},
    {"rut": "20.789.012-7", "nombres": "Antonia", "apellidos": "Castillo"},
    {"rut": "20.890.123-8", "nombres": "Diego", "apellidos": "Guy"},
]

# Actualizar los campos en blanco en la base de datos
for persona in equipo:
    Empleado.objects.filter(rut=persona["rut"]).update(
        nombres=persona["nombres"],
        apellidos=persona["apellidos"]
    )

print("¡Nombres del equipo Jumbo AP actualizados con éxito en la base de datos!")
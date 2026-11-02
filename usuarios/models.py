from django.db import models
from django.contrib.auth.models import User

class PerfilEmpleado(models.Model):
    # Conectamos este perfil directamente al usuario de Django
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    sueldo = models.IntegerField(default=0, verbose_name="Sueldo Base")
    
    # Aquí a futuro podrías agregar: rut, teléfono, dirección, etc.

    def __str__(self):
        return f"Perfil de {self.usuario.username} - ${self.sueldo}"

class Asistencia(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    hora_entrada = models.TimeField(null=True, blank=True)
    hora_salida = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.fecha}"
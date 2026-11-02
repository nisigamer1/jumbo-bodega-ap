from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Crea los grupos de usuarios para la Eva 3'

    def handle(self, *args, **kwargs):
        Group.objects.get_or_create(name='Administrador')
        Group.objects.get_or_create(name='Supervisor')
        Group.objects.get_or_create(name='Administrativo')
        self.stdout.write(self.style.SUCCESS('¡Grupos creados con éxito!'))

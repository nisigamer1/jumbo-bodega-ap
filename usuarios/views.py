from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
import datetime
from .models import Asistencia

# 1. VISTAS DE SESIÓN Y DASHBOARD
def login_view(request):
    # Aquí va tu lógica de login (la que ya tenías funcionando)
    # Ejemplo básico si usas un formulario propio:
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'usuarios/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'usuarios/dashboard_admin.html')

# 2. VISTA DE ASISTENCIA
@login_required(login_url='login')
def marcar_asistencia(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        hoy = timezone.now().date()
        ahora = timezone.now().time()
        usuario = request.user

        asistencia, created = Asistencia.objects.get_or_create(usuario=usuario, fecha=hoy)

        if tipo == 'entrada':
            if asistencia.hora_entrada:
                return JsonResponse({'status': 'info', 'title': 'Aviso', 'msg': 'Ya registraste tu entrada el día de hoy.'})
            
            asistencia.hora_entrada = ahora
            asistencia.save()
            
            if ahora > datetime.time(8, 15): 
                return JsonResponse({'status': 'warning', 'title': 'Llegada Atrasada', 'msg': 'Se ha registrado tu entrada, pero fuera del horario establecido.'})
            
            return JsonResponse({'status': 'success', 'title': '¡Bienvenido!', 'msg': 'Entrada registrada a tiempo.'})

        elif tipo == 'salida':
            if not asistencia.hora_entrada:
                return JsonResponse({'status': 'error', 'title': 'Error', 'msg': 'No puedes marcar salida sin registrar tu entrada primero.'})
            
            if asistencia.hora_salida:
                return JsonResponse({'status': 'info', 'title': 'Aviso', 'msg': 'Ya registraste tu salida el día de hoy.'})
            
            asistencia.hora_salida = ahora
            asistencia.save()

            if ahora > datetime.time(18, 0): 
                return JsonResponse({'status': 'warning', 'title': 'Turno Extendido', 'msg': 'Estás marcando salida más tarde de lo correspondiente.'})
            
            return JsonResponse({'status': 'success', 'title': '¡Buen trabajo!', 'msg': 'Salida registrada correctamente.'})
            
    return JsonResponse({'status': 'error', 'title': 'Error', 'msg': 'Método no permitido.'}, status=405)
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.utils import timezone
import datetime
from .models import Asistencia, PerfilEmpleado

@login_required
def mantenedor_usuarios(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        grupo_nombre = request.POST.get('grupo')
        sueldo = request.POST.get('sueldo', 0)

        # 1. Crear el usuario base de Django
        nuevo_usuario = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # 2. Asignarle el Grupo
        try:
            grupo = Group.objects.get(name=grupo_nombre)
            nuevo_usuario.groups.add(grupo)
        except Group.DoesNotExist:
            pass 

        # 3. Crear perfil con sueldo
        PerfilEmpleado.objects.create(
            usuario=nuevo_usuario,
            sueldo=sueldo
        )
        return redirect('mantenedor_usuarios')

    usuarios = User.objects.select_related('perfil').all()
    grupos = Group.objects.all()
    
    return render(request, 'usuarios/mantenedor_usuarios.html', {
        'usuarios': usuarios,
        'grupos': grupos
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'usuarios/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'usuarios/dashboard_admin.html')

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
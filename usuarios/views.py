from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.utils import timezone
import datetime

from .models import Asistencia, PerfilEmpleado
from usuarios.forms import EditarUsuarioForm, CrearUsuarioForm


def _obtener_o_crear_perfil(user):
    """Obtiene o crea el perfil sin importar si la FK se llama 'user' o 'usuario'."""
    if hasattr(PerfilEmpleado, 'user'):
        perfil, _ = PerfilEmpleado.objects.get_or_create(user=user)
    else:
        perfil, _ = PerfilEmpleado.objects.get_or_create(usuario=user)
    return perfil


def _asignar_sueldo(perfil, monto):
    """Asigna el sueldo sin importar si el campo es 'sueldo_base' o 'sueldo'."""
    if monto is None:
        return
    if hasattr(perfil, 'sueldo_base'):
        perfil.sueldo_base = monto
    elif hasattr(perfil, 'sueldo'):
        perfil.sueldo = monto
    perfil.save()


def _leer_sueldo(perfil):
    """Lee el sueldo de forma segura."""
    return getattr(perfil, 'sueldo_base', getattr(perfil, 'sueldo', 0))


@login_required(login_url='login')
def editar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    perfil = _obtener_o_crear_perfil(usuario)
    
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            nuevo_sueldo = form.cleaned_data.get('sueldo_base')
            if nuevo_sueldo is None or nuevo_sueldo <= 0:
                messages.error(request, 'El sueldo base debe ser mayor a $0.')
                return render(request, 'usuarios/editar_usuario.html', {'form': form, 'usuario': usuario})

            user = form.save()
            
            # 1. Guardar Grupo
            grupo = form.cleaned_data.get('grupo')
            user.groups.clear()
            if grupo:
                user.groups.add(grupo)
                
            # 2. Guardar Sueldo en el Perfil
            _asignar_sueldo(perfil, nuevo_sueldo)
            
            messages.success(request, f'Usuario {user.username} actualizado correctamente.')
            return redirect('mantenedor_usuarios')
    else:
        grupo_actual = usuario.groups.first()
        form = EditarUsuarioForm(
            instance=usuario, 
            initial={'grupo': grupo_actual, 'sueldo_base': _leer_sueldo(perfil)}
        )
        
    return render(request, 'usuarios/editar_usuario.html', {'form': form, 'usuario': usuario})


@login_required(login_url='login')
def mantenedor_usuarios(request):
    if request.method == 'POST':
        form_crear = CrearUsuarioForm(request.POST)
        if form_crear.is_valid():
            sueldo = form_crear.cleaned_data.get('sueldo') or 0
            if sueldo <= 0:
                messages.error(request, 'El sueldo base debe ser mayor a $0.')
            else:
                username = form_crear.cleaned_data['username']
                email = form_crear.cleaned_data['email']
                password = form_crear.cleaned_data['password']
                grupo = form_crear.cleaned_data['grupo']

                # 1. Crear el usuario base de Django
                nuevo_usuario = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )

                # 2. Asignarle el Grupo seleccionable
                if grupo:
                    nuevo_usuario.groups.add(grupo)

                # 3. Crear perfil y asignar sueldo sin fallar
                perfil = _obtener_o_crear_perfil(nuevo_usuario)
                _asignar_sueldo(perfil, sueldo)

                messages.success(request, f'Usuario {username} creado con éxito.')
                return redirect('mantenedor_usuarios')
        else:
            messages.error(request, 'Revisa los datos ingresados. Puede que el usuario ya exista.')
    else:
        form_crear = CrearUsuarioForm()

    usuarios = User.objects.all()
    lista_usuarios = []
    for u in usuarios:
        p = _obtener_o_crear_perfil(u)
        lista_usuarios.append({
            'user': u,
            'sueldo': _leer_sueldo(p)
        })
    
    return render(request, 'usuarios/mantenedor_usuarios.html', {
        'usuarios': lista_usuarios,
        'form_crear': form_crear
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


@login_required(login_url='login')
def eliminar_usuario(request, user_id):
    if request.user.is_superuser or request.user.groups.filter(name='Admin').exists():
        usuario = get_object_or_404(User, id=user_id)
        if usuario != request.user:
            usuario.delete()
            messages.success(request, f'Usuario {usuario.username} eliminado correctamente.')
        else:
            messages.error(request, 'No puedes eliminar tu propio usuario activo.')
    else:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
    return redirect('mantenedor_usuarios')
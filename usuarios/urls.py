from django.urls import path
from . import views
from usuarios import views

urlpatterns = [
    # Esta es la línea clave que falta para que lea el inicio vacio ('')
    path('', views.login_view, name='root_login'), 
    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('marcar-asistencia/', views.marcar_asistencia, name='marcar_asistencia'),
    path('mantenedor-usuarios/', views.mantenedor_usuarios, name='mantenedor_usuarios'),
]

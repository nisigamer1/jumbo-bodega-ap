"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from inventarioapp import views # <-- Este es tu import actual de inventario (déjalo si lo usas)
from usuarios import views as usuarios_views # <-- AGREGA ESTA LÍNEA

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),          
    path('bodega/', include('bodegaApp.urls')),  
    path('inventario/', include('inventarioapp.urls')),
    path('catalogo/', views.catalogo_productos, name='catalogo'),
    path('mantenedor-usuarios/', usuarios_views.mantenedor_usuarios, name='mantenedor_usuarios'),
]


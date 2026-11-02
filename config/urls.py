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
"""
URL configuration for config project.
"""
"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),
    
    # Rutas nativas de autenticación de Django (password_reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Rutas de Usuarios (Login, Dashboard, Mantenedor de Usuarios en la raíz)
    path('', include('usuarios.urls')),
    
    # Rutas de la app Bodega (Menú principal y vistas)
    path('', include('bodegaApp.urls')),
    
    # Rutas de la app Inventario (Productos CRUD)
    path('inventario/', include('inventarioapp.urls')),
]


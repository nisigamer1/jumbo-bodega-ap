from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin de Django
    path('admin/', admin.site.urls),
    
    # 1. Rutas de Usuarios (Tu Login personalizado, Dashboard y Mantenedor)
    path('', include('usuarios.urls')),
    
    # 2. Portada del Sitio y Vistas Públicas de Bodega
    path('', include('bodegaApp.urls')),
    
    # 3. Rutas para la recuperación de clave de Django (APAGADO PARA QUE NO INTERFIERA)
    # path('accounts/', include('django.contrib.auth.urls')),
    
    # 4. Rutas de Inventario
    path('inventario/', include('inventarioapp.urls')),
]
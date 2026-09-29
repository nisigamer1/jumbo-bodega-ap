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
from django.urls import path
from . import views


urlpatterns = [
    path('', views.inicio, name='home_bodega'),                 # <-- Cambiado de 'inicio' a 'home_bodega'
    path('empleados/', views.empleados, name='empleados'),
    path('productos/', views.productos, name='bodega_productos'),
    path('ahora/', views.ahora, name='bodega_ahora'),           # <-- Cambiado de 'ahora' a 'bodega_ahora'
]
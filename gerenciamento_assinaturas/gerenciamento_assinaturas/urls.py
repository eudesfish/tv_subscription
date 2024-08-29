"""
URL configuration for gerenciamento_assinaturas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views

from core import views as core_views
from clientes.views import ClienteListView
from servidores.views import ServidorListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', core_views.dashboard, name='dashboard'),
    path('clientes/', ClienteListView.as_view(), name='clientes'),
    path('servidores/', ServidorListView.as_view(), name='servidores'),
    
    # Inclua as URLs do app assinaturas através do include
    path('assinaturas/', include('assinaturas.urls')),
    path('clientes/', include('clientes.urls')),
    path('servidores/', include('servidores.urls')),
]


from django.urls import path
from . import views

urlpatterns = [

    # ==================================
    # RUTAS WEB DE SOCIOS
    # ==================================

    path('', views.lista_socios, name='lista_socios'),
    path('crear/', views.crear_socio, name='crear_socio'),
    path('editar/<int:pk>/', views.editar_socio, name='editar_socio'),
    path('eliminar/<int:pk>/', views.eliminar_socio, name='eliminar_socio'),

    # ==================================
    # RUTAS API REST DE SOCIOS
    # ==================================

    path('api/socios/', views.api_lista_socios, name='api_lista_socios'),
    path('api/socios/<int:pk>/', views.api_detalle_socio, name='api_detalle_socio'),

]

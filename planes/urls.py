
from django.urls import path
from . import views

urlpatterns = [

    # ==================================
    # RUTAS WEB DE PLANES
    # ==================================

    path('', views.lista_planes, name='lista_planes'),
    path('crear/', views.crear_plan, name='crear_plan'),
    path('editar/<int:pk>/', views.editar_plan, name='editar_plan'),
    path('eliminar/<int:pk>/', views.eliminar_plan, name='eliminar_plan'),

    # ==================================
    # RUTAS API REST DE PLANES
    # ==================================

    path('api/planes/', views.api_lista_planes, name='api_lista_planes'),
    path('api/planes/<int:pk>/', views.api_detalle_plan, name='api_detalle_plan'),

]

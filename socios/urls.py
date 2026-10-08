
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_socios, name='lista_socios'),
    path('crear/', views.crear_socio, name='crear_socio'),
    path('editar/<int:pk>/', views.editar_socio, name='editar_socio'),
    path('eliminar/<int:pk>/', views.eliminar_socio, name='eliminar_socio'),
]

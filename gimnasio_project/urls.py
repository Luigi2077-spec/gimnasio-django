from django.contrib import admin
from django.urls import path, include
from .views import inicio
from .auth_views import api_login, api_logout

urlpatterns = [
    path('', inicio, name='inicio'),
    path('admin/', admin.site.urls),

    # Aplicaciones
    path('planes/', include('planes.urls')),
    path('socios/', include('socios.urls')),

    # Autenticación API
    path('api/login/', api_login, name='api_login'),
    path('api/logout/', api_logout, name='api_logout'),
]
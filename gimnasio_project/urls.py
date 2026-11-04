from django.contrib import admin
from django.urls import path, include
from .views import inicio
from .auth_views import api_login, api_logout
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', inicio, name='inicio'),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),


    # Aplicaciones
    path('planes/', include('planes.urls')),
    path('socios/', include('socios.urls')),

    # Autenticación API
    path('api/login/', api_login, name='api_login'),
    path('api/logout/', api_logout, name='api_logout'),
]
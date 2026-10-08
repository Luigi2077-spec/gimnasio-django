from django.contrib import admin
from django.urls import path, include
from .views import inicio

urlpatterns = [
    path('', inicio, name='inicio'),
    path('admin/', admin.site.urls),
    path('planes/', include('planes.urls')),
    path('socios/', include('socios.urls')),
]
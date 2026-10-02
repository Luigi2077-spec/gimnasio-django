from django.contrib import admin
from .models import Plan


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio', 'duracion_dias', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)
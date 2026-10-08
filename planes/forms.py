
from django import forms
from .models import Plan


class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan

        fields = [
            'nombre',
            'descripcion',
            'precio',
            'duracion_dias',
            'activo',
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del plan',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
            }),
            'duracion_dias': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

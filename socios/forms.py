
from django import forms
from django.db.models import Q

from .models import Socio
from planes.models import Plan


# Validación reutilizable del RUT chileno
def validar_rut(rut):
    # Eliminar puntos, guiones y espacios
    rut = rut.replace('.', '').replace('-', '').replace(' ', '').upper()

    if len(rut) < 2:
        raise forms.ValidationError(
            'El RUT ingresado no es válido.'
        )

    numero = rut[:-1]
    digito_verificador = rut[-1]

    if not numero.isdigit():
        raise forms.ValidationError(
            'El RUT debe contener números válidos.'
        )

    # Calcular dígito verificador mediante módulo 11
    suma = 0
    multiplicador = 2

    for digito in reversed(numero):
        suma += int(digito) * multiplicador
        multiplicador += 1

        if multiplicador > 7:
            multiplicador = 2

    resultado = 11 - (suma % 11)

    if resultado == 11:
        digito_calculado = '0'
    elif resultado == 10:
        digito_calculado = 'K'
    else:
        digito_calculado = str(resultado)

    if digito_verificador != digito_calculado:
        raise forms.ValidationError(
            'El dígito verificador del RUT es incorrecto.'
        )

    # Devolver el RUT normalizado
    return f'{numero}-{digito_verificador}'


# Validación reutilizable del teléfono
def validar_telefono(telefono):
    telefono = telefono.replace(' ', '').replace('-', '')

    if not telefono.startswith('+569'):
        raise forms.ValidationError(
            'El teléfono debe comenzar con +569.'
        )

    if len(telefono) != 12:
        raise forms.ValidationError(
            'El teléfono debe tener el formato +569XXXXXXXX.'
        )

    if not telefono[1:].isdigit():
        raise forms.ValidationError(
            'El teléfono solo debe contener números.'
        )

    return telefono


class SocioForm(forms.ModelForm):

    class Meta:
        model = Socio

        fields = [
            'nombre',
            'apellido',
            'rut',
            'correo',
            'telefono',
            'plan',
            'activo'
        ]

        widgets = {
            'nombre': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'apellido': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'rut': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'correo': forms.EmailInput(
                attrs={'class': 'form-control'}
            ),
            'telefono': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'plan': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'activo': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        planes = Plan.objects.filter(activo=True)

        # Si el socio ya tiene un plan asignado,
        # también permitir mostrar ese plan aunque esté inactivo.
        if self.instance.pk and self.instance.plan_id:
            planes = Plan.objects.filter(
                Q(activo=True) | Q(pk=self.instance.plan_id)
            )

        self.fields['plan'].queryset = planes
        self.fields['plan'].empty_label = 'Sin plan asignado'

    def clean_rut(self):
        rut = self.cleaned_data['rut']
        return validar_rut(rut)

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        return validar_telefono(telefono)
